"""
سجل مساهمات المشروع الجماعي - نموذج أولي
كل عضو بالقروب يسجل الجزء اللي سلّمه، والسجل يكون سلسلة كتل
عشان محد يقدر يغيّر أو ينسب شغل غيره لنفسه بعدين.
"""

import hashlib
import json
from datetime import datetime


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Block:
    def __init__(self, index, member, task, work_hash, previous_hash):
        self.index = index
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.member = member
        self.task = task
        self.work_hash = work_hash  # بصمة الملف المسلّم مو الملف نفسه
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "member": self.member,
            "task": self.task,
            "work_hash": self.work_hash,
            "previous_hash": self.previous_hash,
        }
        return sha256(json.dumps(data, sort_keys=True))


class ContributionChain:
    def __init__(self, project_name):
        self.project_name = project_name
        self.chain = [Block(0, "system", "project created: " + project_name, "-", "0")]

    def add_contribution(self, member, task, work_content):
        last = self.chain[-1]
        block = Block(len(self.chain), member, task, sha256(work_content), last.hash)
        self.chain.append(block)
        return block

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False, f"block {i} was modified (its hash doesn't match its data)"
            if current.previous_hash != previous.hash:
                return False, f"block {i} is no longer linked to block {i - 1}"
        return True, "chain is valid"

    def verify_file(self, block_index, work_content):
        # الدكتور يتأكد إن الملف اللي عنده هو نفس اللي انسجل
        return self.chain[block_index].work_hash == sha256(work_content)

    def summary(self):
        counts = {}
        for block in self.chain[1:]:
            counts[block.member] = counts.get(block.member, 0) + 1
        return counts

    def print_chain(self):
        for b in self.chain:
            print(f"[{b.index}] {b.timestamp} | {b.member:<8} | {b.task}")
            print(f"     prev: {b.previous_hash[:16]}...  hash: {b.hash[:16]}...")


def check(chain):
    ok, msg = chain.is_valid()
    print(("OK  -> " if ok else "TAMPERING DETECTED -> ") + msg)


if __name__ == "__main__":
    project = ContributionChain("CS-HCI Group 4")

    project.add_contribution("Turki", "wrote the introduction", "Introduction text v1 ...")
    project.add_contribution("Sara", "designed the slides", "slides.pptx content ...")
    project.add_contribution("Faisal", "added references", "references list ...")
    project.add_contribution("Turki", "built the prototype", "prototype source code ...")

    print("=== Contribution log ===")
    project.print_chain()
    print()
    check(project)
    print("Contributions per member:", project.summary())

    # الدكتور يتحقق من ملف السلايدات
    print("Slides file matches record?", project.verify_file(2, "slides.pptx content ..."))

    # محاولة تلاعب 1: فيصل يغيّر اسم صاحب السلايدات لاسمه
    print("\n=== Tamper attempt 1: Faisal changes block 2 to his name ===")
    project.chain[2].member = "Faisal"
    check(project)

    # محاولة تلاعب 2: يعيد حساب هاش الكتلة عشان يخفي التعديل
    print("\n=== Tamper attempt 2: he also recalculates block 2's hash ===")
    project.chain[2].hash = project.chain[2].calculate_hash()
    check(project)
