#-*- encoding:UTF-8 -*-
import random
import log

class Card():

    # 0黑1红
    colors = ("0", "1", "1", "0")
    # 花色的值按列表的排序
    kinds = ("♣", "♦", "♥", "♠")
    indexs = {"3":0, "4":4, "5":8, "6":12, "7":16, "8":20, "9":24, "10":28, "J":32, "Q":36, "K":40, "A":44, "2":48, "Joker":52}
    names = ("3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "2", "Joker")
    # 对应牌的张数
    nums = (4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2)

    def __init__(self, index=None, name=None, kind=None):
        self.name = name
        self.kind = kind
        self.index = index
        if index is None:
            self.index = Card.indexs[self.name] + self.kind
        else:
            self.name = Card.names[self.index / 4]
            self.kind = self.index % 4
        self.color = Card.colors[self.kind]

    def show(self):
        return "%s%s\t" % (Card.kinds[self.kind], self.name)

class Cards():

    class_name = "Cards"
    kinds = ("单牌", "双对", "三对", "三带一", "三带二", "单顺", "双顺", "三顺", "四顺", "三顺带单", "三顺带双", "四顺带二单", "四顺带二对", "炸弹", "火箭", "杂牌")
    # 最小数量，等于
    count_min = (1, 2, 3, 4, 5, 5, 6, 6, 8, 8, 10, 6, 8, 4, 2, 0)
    # 最大数量，不等于
    count_max = (2, 3, 4, 5, 6, 13, 21, 19, 21, 17, 16, 19, 17, 5, 3, 1)
    # 步长值
    count_step = (1, 1, 1, 1, 1, 1, 2, 3, 4, 4, 5, 6, 8, 1, 1, 1)
    # 每种牌的最大值
    value_max = (13, 12, 12, 12, 12, 11, 11, 11, 11, 11, 11, 12, 12, 12, 54)

    def __init__(self, cards = None, indexs = None):
        self.cards = []
        self.values = []
        self.kind = -1
        self.value = -1
        if indexs is not None:
            self.indexs = indexs
            for index in self.indexs:
                self.cards.append(Card(index))
                self.values.append(index / 4)
        elif cards is not None:
            self.indexs = []
            self.cards = cards
            for card in self.cards:
                self.indexs.append(card.index)
                self.values.append(card.index / 4)
        else:
            self.indexs = []
            while len(self.indexs) < 54:
                r = random.randint(0, 53)
                if r not in self.indexs:
                    self.indexs.append(r)
                    self.values.append(r / 4)
                    self.cards.append(Card(r))

    # 洗牌
    def shuffle(self):
        method_name = "shuffle"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        tmp_indexs = self.indexs
        tmp_cards = self.cards
        tmp_random = []
        self.indexs = []
        self.values = []
        self.cards = []
        while len(tmp_random) < len(tmp_indexs):
            r = random.randint(0, len(tmp_indexs) - 1)
            if r not in tmp_random:
                tmp_random.append(r)    
                self.indexs.append(tmp_indexs[r])
                self.values.append(tmp_indexs[r] / 4)
                self.cards.append(tmp_cards[r])
        tmp_indexs = None
        tmp_cards = None
        tmp_random = None
        return self.cards

    def sort_cards(self):
#        method_name = "sort_cards"
#        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        tmp_cards = []
        for card in self.cards:
            tmp_cards.append((card.index, card))
        tmp_cards.sort()
        self.cards = []
        self.indexs.sort()
        self.values.sort()
        for tmp in tmp_cards:
            self.cards.append(tmp[1])
        tmp_cards = None
        return self

    def rebuild(self):
        method_name = "rebuild"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        self.cards = []
        for index in self.indexs:
            self.cards.append(Card(index))

    def append(self, cards):
#        method_name = "append"
#        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        self.cards.extend(cards)
        for card in cards:
            self.indexs.append(card.index)
            self.values.append(card.index / 4)
        return self.cards
        
    def remove(self, cards):
#        method_name = "remove"
#        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        for card in cards:
            self.cards.remove(card)
            self.indexs.remove(card.index)
            self.values.append(card.index / 4)
        return self.cards
    
    def show(self, show_index = True):
        method_name = "show"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        show_str = ""
        if show_index:
            for i in range(len(self.cards)):
                show_str = "%s%d\t" % (show_str, i)
            show_str = "%s\n" % show_str
        for card in self.cards:
            show_str = "%s%s" % (show_str, card.show())
        return show_str

    def size(self):
        method_name = "size"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)
        return len(self.cards)

    def compare(self, compare_to_cards):
        method_name = "compare"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        if self.kind == -1:
            return -99
        kind_come, value_come = (compare_to_cards.kind, compare_to_cards.value)
        if self.kind == kind_come:
            if self.size() == compare_to_cards.size():
                if self.value == 13 and value_come == 13:
                    return cmp(self.indexs[0], compare_to_cards.indexs[0])
                else:
                    return cmp(self.value, value_come)
            else:
                return -99
        else:
            if self.kind < 12 and kind_come < 12:
                return -99
            else:
                return cmp(self.kind, kind_come)

    def get_kind_value(self):
        method_name = "get_kind_value"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        count = self.sort_cards().size()
        self.kind, self.value = (-1, -1)
        for i in range(len(Cards.kinds) - 1):
            if count in range(Cards.count_min[i], Cards.count_max[i], Cards.count_step[i]):
                self.kind, self.value = eval("self.is_kind%d()" % i)
                if self.kind != -1:
                    break
        return (self.kind, self.value)

    # 返回顺子的最大值
    def is_order(self, values):
        value = values[0]
        if len(values) == 1:
            return value
        for i in values[1:]:
            if (i - value) != 1 or i > Cards.value_max[5]:
                return -1
            value = i
        return values[-1]
    # 单牌
    def is_kind0(self):
        method_name = "is_kind0"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        return (0, self.values[0])
    # 双对
    def is_kind1(self):
        method_name = "is_kind1"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        value = self.get_same_value(self.values)
        if value == -1:
            return (-1, -1)
        elif value == 13:
            return (13, 13)
        else:
            return (1, value)
    # 三对
    def is_kind2(self):
        method_name = "is_kind2"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        value = self.get_same_value(self.values)
        if value == -1:
            return (-1, -1)
        else:
            return (2, value)
    # 三带一
    def is_kind3(self):
        method_name = "is_kind3"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        for value in self.values[0:2]:
            if self.values.count(value) == 3:
                return (3, value)
        return (-1, -1)
    # 三带二
    def is_kind4(self):
        method_name = "is_kind4"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        if self.get_same_value(self.values[:2]) != -1 and\
                self.get_same_value(self.values[2:]) != -1:
            return (4, self.values[-1])
        if self.get_same_value(self.values[:3]) != -1 and\
                self.get_same_value(self.values[3:]) != -1:
            return (4, self.values[0])
        return (-1, -1)
    # 单顺
    def is_kind5(self):
        method_name = "is_kind5"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        value = self.is_order(self.values)
        if value != -1:
            return (5, value)
        else:
            return(-1, -1)
    # 双顺
    def is_kind6(self):
        method_name = "is_kind6"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        size = len(self.values)
        value = self.values[0]
        if value != self.values[1]:
            return (-1, -1)
        for i in range(2 , size, 2):
            if self.values[i] != self.values[i + 1] or (self.values[i] - value) != 1 or self.values[i] > Cards.value_max[6]:
                return (-1, -1)
            value = self.values[i]
        return (6, self.values[-1])
    # 三顺
    def is_kind7(self):
        method_name = "is_kind7"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        size = len(self.values)
        value = self.values[0]
        if value != self.values[1] or value != self.values[2]:
            return (-1, -1)
        for i in range(3 , size, 3):
            if self.values[i] != self.values[i + 1] or self.values[i] != self.values[i + 2]\
                    or (self.values[i] - value) != 1 or self.values[i] > self.value_max[7]:
                return (-1, -1)
            value = self.values[i]
        return (7, self.values[-1])
    # 四顺
    def is_kind8(self):
        method_name = "is_kind8"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        size = len(self.values)
        tmp_values = []
        i = 0
        while i < size:
            count = self.values.count(self.values[i])
            if self.values[i] > self.value_max[8] or count != 4:
                return(-1, -1)
            tmp_values.append(self.values[i])
            i += count
        value = self.is_order(tmp_values)
        if value != -1:
            tmp_values = None
            return(8, value)
        return (-1, -1)
    # 三顺带单
    def is_kind9(self):
        method_name = "is_kind9"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        size = len(self.values)
        tmp_values = []
        i = 0
        while i < size:
            count = self.values.count(self.values[i])
            if self.values[i] <= self.value_max[9] and count >= 3:
                tmp_values.append(self.values[i])
            i += count
        if len(tmp_values) > size / self.count_step[9]:
            value = self.is_order(tmp_values[1:])
            if value != -1:
                tmp_values = None
                return(9, value)
            value = self.is_order(tmp_values[:-1])
            if value != -1:
                tmp_values = None
                return(9, value)
        elif len(tmp_values) == size / self.count_step[9]:
            value = self.is_order(tmp_values)
            if value != -1:
                tmp_values = None
                return(9, value)
        return (-1, -1)
    # 三顺带双
    def is_kind10(self):
        method_name = "is_kind10"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        size = len(self.values)
        tmp_values = []
        i = 0
        while i < size:
            count = self.values.count(self.values[i])
            if self.values[i] <= self.value_max[10] and count == 3:
                tmp_values.append(self.values[i])
            elif count % 2 != 0:
                return(-1, -1)
            i += count

        if len(tmp_values) == size / 5:
            value = self.is_order(tmp_values)
            if value != -1:
                tmp_values = None
                return(10, value)
        return (-1, -1)
    # 四顺带二单
    def is_kind11(self):
        method_name = "is_kind11"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        size = len(self.values)
        tmp_values = []
        i = 0
        while i < size:
            count = self.values.count(self.values[i])
            if self.values[i] <= self.value_max[11] and count == 4:
                tmp_values.append(self.values[i])
            i += count
        if len(tmp_values) > size / self.count_step[11]:
            value = self.is_order(tmp_values[1:])
            if value != -1:
                tmp_values = None
                return(11, value)
            value = self.is_order(tmp_values[:-1])
            if value != -1:
                tmp_values = None
                return(11, value)
        elif len(tmp_values) == size / self.count_step[11]:
            value = self.is_order(tmp_values)
            if value != -1:
                tmp_values = None
                return(11, value)
        return (-1, -1)
    # 四顺带二对
    def is_kind12(self):
        method_name = "is_kind12"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        size = len(self.values)
        tmp_values = []
        i = size - 1
        while i >= 0:
            count = self.values.count(self.values[i])
            if self.values[i] <= self.value_max[10] and count == 4:
                tmp_values.append(self.values[i])
            elif count % 2 != 0:
                return(-1, -1)
            i -= count

        if len(tmp_values) == size / self.count_step[12]:
            value = self.is_order(tmp_values)
            if value != -1:
                tmp_values = None
                return(12, value)
        elif len(tmp_values) > size / self.count_step[12]:
            value = tmp_values[0]
            for i in tmp_values[1:]:
                if value - i == 1:
                    return (12, value)
                value = i
        return (-1, -1)
    # 炸弹
    def is_kind13(self):
        method_name = "is_kind13"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        value = self.get_same_value(self.values)
        if value == -1:
            return (-1, -1)
        else:
            return (13, value)
    # 火箭
    def is_kind14(self):
        method_name = "is_kind14"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        value = self.get_same_value(self.values)
        if value == -1:
            return (-1, -1)
        elif value == 13:
            return (14, 13)
        else:
            return (1, value)
    # 取得相同的值
    def get_same_value(self, values):
        method_name = "get_same_value"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        if values.count(values[0]) != len(values):
            return -1
        else:
            return values[0]

class Player():

    class_name = "Player"

    def __init__(self, name, pos, order, role = None, cards = None):
        self.name = name
        self.pos = pos
        self.order = order
        self.score = 0
        if cards is None:
            self.cards = Cards([])
        else:
            self.cards = cards

    # 叫分
    def bet(self):
        method_name = "bet"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        bet = input("bet>>")
        while bet not in range(0,4):
            bet = input("bet>>")
        return bet

    def say(self):
        method_name = "say"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        print "name:%s, score:%s" % (self.name, self.score)
        
    def show(self, show_index = True):
        method_name = "show"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)
        return "%s\n%s" % (self.name, self.cards.show(show_index))

    # 摸牌
    def get_cards(self, cards):
#        method_name = "get_cards"
#        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        self.cards.append(cards)
        return self

    # 出牌
    def out_cards(self, cards):
#        method_name = "out_cards"
#        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        self.cards.remove(cards)
        return self

    def sort_cards(self):
#        method_name = "sort_cards"
#        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        self.cards.sort_cards()
        return self

    # 选牌
    def play(self, round_cards = None):
        method_name = "play"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        if round_cards is not None:
            print '===================== play ========================='
            log.log_class(self.class_name, method_name, "\n%s %s" %\
                           (Cards.kinds[round_cards.kind], round_cards.show(False)), log.LOG_INFO)
        print "======"
        print self.show()
        print "======"
        judge_result = -1
        while judge_result < 1:
            self.select = Cards([])
            select_tmp = []
            select_index = raw_input("play>>").split()
            for i in select_index:
                # index重复或超过最大值
                if select_index.count(i) > 1 or int(i) >= self.cards.size():
                    select_index = None
                    break
                select_tmp.append(self.cards.cards[int(i)])
            if select_index is None:
                continue
            self.select.append(select_tmp)
            self.select.get_kind_value()
            if round_cards is None:
                if self.select.size() == 0 or self.select.kind == -1:
                    continue
                else:
                    break
            else:
                if self.select.size() == 0:
                    break
                else:
                    judge_result = self.select.compare(round_cards)
        # 未Pass，更新出牌和手牌
        if self.select.size() > 0:
            self.out_cards(self.select.cards)
        return self.select

class Game():

    class_name = "Game"

    def __init__(self, player_count = 3):
        # 玩家数
        self.player_count = player_count
        # 玩家列表
        self.players = []
        # 玩家初始化
        for i in range(self.player_count):
            self.players.append(Player("player%d" % (i+1), i, i))

    def start(self):
        method_name = "start"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        # 牌堆
        self.heap = Cards(indexs = range(0, 54))
        all_cards = self.heap.shuffle()
        # 已出牌
        self.drop_cards = Cards([])
        # 回合数
        self.round = 0
        # 本回合已出牌
        self.round_drops = Cards([])
        # 初始摸牌数
        get_count = 51
        #一次性摸牌
#        card_count = len(all_cards)
#        n = 0
#        for i in range(self.player_count):
#            if i <= card_count % self.player_count - 1:
#                get_count = card_count / self.player_count + 1
#            else:
#                get_count = card_count / self.player_count
#            self.players[i].get_cards(all_cards[n:n + get_count])
#            n += get_count
        
        #顺序摸牌
        for i in range(get_count):
            self.players[i % self.player_count].get_cards([all_cards[0]])
            # 从牌堆中移除玩家摸走的牌
            self.heap.remove([all_cards[0]])

        # 下注
        self.bet = 0
        # 番
        self.rate = 1
        self.landlord = None

        for player in self.players:
            player.sort_cards()
        for player in self.players:
            print player.show(False)
            bet = int(player.bet())
            if bet >= self.player_count:
                self.bet = bet
                self.landlord = player
                break
            elif bet > self.bet:
                self.bet = bet
                self.landlord = player
        if self.bet == 0:
            self.start()

        self.landlord.get_cards(self.heap.cards).sort_cards()
        self.heap.remove(self.heap.cards)
        self.round_start(self.landlord)

    def round_start(self, player):
        method_name = "round_start"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        log.log_class(self.class_name, method_name, " -------- new round start --------", log.LOG_INFO)
        self.round += 1
        pass_count = 0
        round_cards = player.play()
        if round_cards.kind == 13 or round_cards.kind == 14:
            self.rate *= 2
        if player.cards.size() == 0:
            self.end(player)
        round_winner = player
        self.drop_cards.append(round_cards.cards)
        while True:
            player = self.next_player(player)
            round_cards = player.play(round_winner.select)
            if round_cards.size() == 0:
                pass_count += 1
                log.log_class(self.class_name, method_name, pass_count)
                if pass_count == self.player_count - 1:
                    self.round_start(round_winner)
            elif player.cards.size() == 0:
                self.end(player)
            else:
                pass_count = 0
                round_winner = player
                self.drop_cards.append(round_cards.cards)
                if round_cards.kind == 13 or round_cards.kind == 14:
                    self.rate *= 2

    def next_player(self, player):
        method_name = "next_player"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)

        index = self.players.index(player)
        if index == self.player_count - 1:
            next_player = self.players[0]
        else:
            next_player = self.players[index + 1]
        return next_player

    def end(self, winner):
        method_name = "end"
        log.log_class(self.class_name, method_name, level=log.LOG_DEBUG, show_console = False)
        if self.round == 1:
            self.rate *= 2
        if self.landlord == winner:
            self.landlord.score += self.bet * self.rate * 2
        else:
            self.landlord.score -= self.bet * self.rate * 2
        self.landlord.say()
        for player in self.players:
            player.cards = Cards([])
            player.select = Cards([])
            if player == self.landlord:
                continue
            if self.landlord == winner:
                player.score -= self.bet * self.rate
            else:
                player.score += self.bet * self.rate
            player.say()
        con = raw_input("1:继续 0:结束>>")

        self.heap = None
        self.drop_cards = None
        self.round_drops = None
        if con == "1":
            self.start()
        else:
            self.players = None

game = Game()
game.start()
#cards = Cards(indexs=[32,33,34,35,36,37,38,39,40,41,42,43,48,49,50,51])
#kind, value = cards.get_kind_value()
#print cards.show(show_index = False)
#print Cards.kinds[kind],value
