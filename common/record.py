class Step_Record:
    def __init__(self, count, color):
        self.count = count
        self.color = color


class Record:
    def __init__(self):
        self.count = 1
        self.records = [[None for i in range(15)] for j in range(15)]

    def has_record(self, x, y):
        return self.records[x][y] is not None

    def insert_record(self, x, y, color):
        self.records[x][y] = Step_Record(self.count, color)
        self.count += 1

    def delete_record(self, x, y):
        self.records[x][y] = None
        self.count -= 1

    def who_to_play(self):
        return (self.count) % 2 + 1

    def check_row(self, x, y):
        if self.has_record(x, y) and self.has_record(x, y+1) and self.has_record(x, y+2) and self.has_record(x, y+3) and self.has_record(x, y+4):
            # 判断一个子右侧是否5个连续有子,如果是判断是否连续的黑色或者白色,返回1或者2代表胜利
            # print(self.records[x][y].color)
            # print(self.records[x][y+1].color)
            # print(self.records[x][y+2].color)
            # print(self.records[x][y+3].color)
            # print(self.records[x][y+4].color)
            if self.records[x][y].color == 'white' and self.records[x][y+1].color == 'white' and self.records[x][y+2].color == 'white' and self.records[x][y+3].color == 'white' and self.records[x][y+4].color == 'white':# noqaE501
                return 1

            elif self.records[x][y].color == 'black' and self.records[x][y+1].color == 'black' and self.records[x][y+2].color == 'black' and self.records[x][y+3].color == 'black' and self.records[x][y+4].color == 'black':# noqaE501
                return 2

        else:
            return 0

    def check_col(self, x, y):
        if self.has_record(x, y) and self.has_record(x+1, y) and self.has_record(x+2, y) and self.has_record(x+3, y) and self.has_record(x+4, y):

            if self.records[x][y].color == 'white' and self.records[x+1][y].color == 'white' and self.records[x+2][y].color == 'white' and self.records[x+3][y].color == 'white' and self.records[x+4][y].color == 'white':# noqaE501
                print(self.records[x][y].color)
                return 1

            elif self.records[x][y].color == 'black' and self.records[x+1][y].color == 'black' and self.records[x+2][y].color == 'black' and self.records[x+3][y].color == 'black' and self.records[x+4][y].color == 'black':# noqaE501
                return 2

        else:
            return 0

    def check_up(self, x, y):
        if x + 4 < 15 and y + 4 < 15:
            if self.has_record(x, y) and self.has_record(x+1, y+1) and self.has_record(x+2, y+2) and self.has_record(x+3, y+3) and self.has_record(x+4, y+4):

                if self.records[x][y].color == 'white' and self.records[x+1][y+1].color == 'white' and self.records[x+2][y+2].color == 'white' and self.records[x+3][y+3].color == 'white' and self.records[x+4][y+4].color == 'white':# noqaE501
                    return 1# noqaE501

                elif self.records[x][y].color == 'black' and self.records[x+1][y+1].color == 'black' and self.records[x+2][y+2].color == 'black' and self.records[x+3][y+3].color == 'black' and self.records[x+4][y+4].color == 'black':# noqaE501
                    return 2
            else:
                return 0
        else:
            return 0

    def check_down(self, x, y):
        if x + 4 < 15 and y - 4 >= 0:
            if self.has_record(x, y) and self.has_record(x+1, y-1) and self.has_record(x+2, y-2) and self.has_record(x+3, y-3) and self.has_record(x+4, y-4):

                if self.records[x][y].color == 'white' and self.records[x+1][y-1].color == 'white' and self.records[x+2][y-2].color == 'white' and self.records[x+3][y-3].color == 'white' and self.records[x+4][y-4].color == 'white':# noqaE501
                    return 1

                elif self.records[x][y].color == 'black' and self.records[x+1][y-1].color == 'black' and self.records[x+2][y-2].color == 'black' and self.records[x+3][y-3].color == 'black' and self.records[x+4][y-4].color == 'black':# noqaE501
                    return 2
            else:
                return 0
        else:
            return 0

    def check(self):
        for i in range(15):
            for j in range(11):
                result = self.check_row(i, j)
                if result != 0:
                    return result

        for i in range(11):
            for j in range(15):
                result = self.check_col(i, j)
                if result != 0:
                    return result

        for i in range(15):
            for j in range(15):
                result = self.check_up(i, j)
                if result != 0:
                    return result

        for i in range(15):
            for j in range(15):
                result = self.check_down(i, j)
                if result != 0:
                    return result
