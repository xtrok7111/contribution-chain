# سجل مساهمات المشروع الجماعي
# كل عضو يسجل الجزء اللي سلمه وكل بلوك مربوط باللي قبله

import hashlib
from datetime import datetime


class Block:
    def __init__(self, index, member, task, previous_hash):
        self.index = index
        self.time = str(datetime.now())
        self.member = member
        self.task = task
        self.previous_hash = previous_hash
        self.hash = self.get_hash()

    def get_hash(self):
        data = str(self.index) + self.time + self.member + self.task + self.previous_hash
        return hashlib.sha256(data.encode()).hexdigest()


class Chain:
    def __init__(self):
        # اول بلوك
        self.blocks = [Block(0, "start", "project created", "0")]

    def add(self, member, task):
        last = self.blocks[-1]
        self.blocks.append(Block(len(self.blocks), member, task, last.hash))

    def is_valid(self):
        for i in range(1, len(self.blocks)):
            block = self.blocks[i]
            before = self.blocks[i - 1]

            # اذا البيانات تغيرت الهاش ما يطابق
            if block.hash != block.get_hash():
                print("block", i, "was changed")
                return False

            # اذا الربط انكسر مع اللي قبله
            if block.previous_hash != before.hash:
                print("block", i, "is not linked to block", i - 1)
                return False

        print("chain is valid")
        return True


project = Chain()
project.add("Turki", "introduction")
project.add("Sara", "slides")
project.add("Faisal", "references")
project.add("Turki", "code")

for b in project.blocks:
    print(b.index, b.member, b.task, b.hash[:10])

project.is_valid()

# تلاعب: فيصل يحط اسمه على السلايدات
print("\nFaisal changes the slides to his name")
project.blocks[2].member = "Faisal"
project.is_valid()

# يحاول يخفي التعديل ويعيد حساب الهاش
print("\nhe recalculates the hash")
project.blocks[2].hash = project.blocks[2].get_hash()
project.is_valid()
