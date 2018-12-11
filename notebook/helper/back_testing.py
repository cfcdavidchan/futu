import json, random
from collections import Counter


class back_testing():
    def __init__(self, inventory_limit = 1):
        
        self.order_book = dict() ## save all the trade order, format  {'order_number': {'Time': time string, 'Book_Value': int(), 'Position':int()}}
        
        self.inventory = dict()
        self.inventory['Long'] = []
        self.inventory['Short'] = []
        
        #self.inventory_holding = len(self.inventory['Long']) - len(self.inventory['Short'])
        
        self.PnL = 0
        
        self.record = dict() ## record format {'abc': {'p and l': 0}}
        
        self.current_opening = [] ## store the opened order number 
        
        self.order_number_i = 1
        
        self.inventory_limit = inventory_limit
        
        self.book_value_high = []
        self.book_value_low = []
        self.book_value_open = []
        self.book_value_close = []
        
        
    def order_number_create(self):
        
        order_number = "%.5d"% self.order_number_i ## create 5 digital order number e.g. 00001, 00050
        self.order_number_i += 1 ## update the number 
        
        return order_number ## return a order number
    
    
    
    def open_position(self, order_time, position, price,  order_number= True):
        if abs(self.current_holding()) >= self.inventory_limit: ## abs is for converting short position to a abs value
            print (order_time)
            print ('Order Rejected')
            print ('Current inventroy ( %d lots) exceed/equal to the inventory limited %d' %(self.inventory, self.inventory_limit))
            return
    
        else:
            order_number = self.order_number_create()
            self.current_opening.append(order_number)
            self.order(order_time, position, price, order_number= order_number) ## create an order
            if position > 0:
                self.inventory['Long'].append(price)
            
            if position < 0:
                self.inventory['Short'].append(price)
            
            return self.current_opening
            
            
    def close_position(self, order_time, position, price, order_number):
        if self.inventory == 0:
            print ('Current inventroy = %d,  Close position Reject!'%(self.inventory))
            
        if order_number not in self.current_opening:
            print ('%s not exiting in the inventory')
        
        
        else:
            self.order(order_time, position, price, order_number= order_number) ## create an order
            self.current_opening.remove(order_number)
            
            if position > 0:
                self.inventory['Short'].pop()
            
            if position < 0:
                self.inventory['Long'].pop()
            
            print ('P and L:',self.order_book[order_number]['Out price'] + self.order_book[order_number]['In price'])
            

            
            
    
    def order(self, order_time, position, price, order_number):
        #if order_number == True: ## using order number function
        #    order_number= self.order_number_create
        if order_number not in self.order_book:
            self.order_book[order_number] = dict()
            self.order_book[order_number]['In time'] = order_time
            self.order_book[order_number]['In position'] = position
            self.order_book[order_number]['In price'] = price
        
        else:
            self.order_book[order_number]['Out time'] = order_time
            self.order_book[order_number]['Out position'] = position
            self.order_book[order_number]['Out price'] = price
            
            self.order_book[order_number]['Holding period'] = self.order_book[order_number]['Out time'] - self.order_book[order_number]['In time']
            
            self.order_book[order_number]['point earn'] = self.order_book[order_number]['Out price'] + self.order_book[order_number]['In price']
            
            
            self.PnL += (self.order_book[order_number]['Out price'] + self.order_book[order_number]['In price'])* abs(self.order_book[order_number]['Out position']) ## Profit Released
            print (self.PnL)
     
    def current_holding(self):
        return len(self.inventory['Long']) - len(self.inventory['Short'])
    
    
    def inventory_status(self, open_price = None, high_price = None, low_price = None, close_price = None):
        
        if self.current_holding() == 0:
            return

        else:
            if close_price == None:
                print ('Current Inventory: %d\nBook Value is required to input)'% self.current_holding())
            else:
                if self.current_holding() > 0:
                        self.book_value_open.append(self.inventory['Long'][0] + open_price)
                        self.book_value_high.append(self.inventory['Long'][0] + high_price)
                        self.book_value_low.append(self.inventory['Long'][0] + low_price)
                        self.book_value_close.append(self.inventory['Long'][0] + close_price)
                elif self.current_holding() < 0:
                        self.book_value_open.append(self.inventory['Short'][0] - open_price)
                        self.book_value_high.append(self.inventory['Short'][0] - high_price)
                        self.book_value_low.append(self.inventory['Short'][0] - low_price)
                        self.book_value_close.append(self.inventory['Short'][0] - close_price)
        
                print ('Book Value @ Open: %d' %self.book_value_open[-1])
                print ('Book Value @ High: %d' %self.book_value_high[-1])
                print ('Book Value @ Low: %d' %self.book_value_low[-1])
                print ('Book Value @ Close: %d\n\n' %self.book_value_close[-1])

        return [self.book_value_open[-1], self.book_value_high[-1], self.book_value_low[-1], self.book_value_close[-1]]
    
    def profit_and_loss(self):
        return self.PnL, self.order_book
    
    
    def trading_summary(self, point_price = 50):
        summary = dict()
        
        P_L_point = self.PnL
        P_L_Money = P_L_point * point_price
        summary['Point Earning'] = P_L_point
        summary['Money Earning'] = P_L_Money
        
        hold_period = [value['Holding period'] for key,value in self.order_book.items()]
        max_period = max(hold_period)
        min_period = min(hold_period)
        summary['Max Holding Period'] = max_period
        summary['Min Holding Period'] = min_period
        
        
        point = [value['point earn'] for key,value in self.order_book.items()]
        max_point = max(point)
        min_point = min(point)
        summary['Max Point Earning'] = max_point
        summary['Min Point Earning'] = min_point
        summary['Average point earning'] = sum(point)/len(point)
        
        
        max_book_open = max(self.book_value_open)
        min_book_open = min(self.book_value_open)
        max_book_high = max(self.book_value_high)
        min_book_high = min(self.book_value_high)
        max_book_low = max(self.book_value_low)
        min_book_low = min(self.book_value_low)
        max_book_close = max(self.book_value_close)
        min_book_close = min(self.book_value_close)
        
        summary['Max Book Value @ open'] = max_book_open
        summary['Min Book Value @ open'] = min_book_open
        summary['Max Book Value @ high'] = max_book_high
        summary['Min Book Value @ high'] = min_book_high
        summary['Max Book Value @ low'] = max_book_low
        summary['Min Book Value @ low'] = min_book_low
        summary['Max Book Value @ close'] = max_book_close
        summary['Min Book Value @ close'] = min_book_close
        
        summary['number_of_trade'] = len(self.order_book) * 2
        
        
        summary['per point sumaary'] = dict()
        
        point_earn_list = [v['point earn']for k,v in self.order_book.items()]
        point_counter = Counter(point_earn_list)
        point_dict = dict(point_counter)
        
        total_trade = len(point)
        ev = 0
        for key, item in point_dict.items():
            ev += (key * (item/total_trade))
        
        summary['per point sumaary']['Expected Value per trade'] = ev
        
        win = [key for key in point_dict.keys() if key >0]
        loss = [key for key in point_dict.keys() if key <=0]

        win_rate = len(win) / len(point_dict)
        loss_rate = len(loss) / len(point_dict)

        average_win = sum(win)/len(win)
        average_loss = sum(loss)/len(loss)

        max_win = max(win)
        min_win = min(win)

        max_loss = min(loss)
        min_loss = max(loss)

        summary['per point sumaary']['win rate'] = win_rate
        summary['per point sumaary']['loss rate'] = loss_rate
        
        summary['per point sumaary']['average win point'] = average_win
        summary['per point sumaary']['average loss point'] = average_loss
        
        summary['per point sumaary']['max win'] = max_win
        summary['per point sumaary']['min win'] = min_win
        
        summary['per point sumaary']['max loss'] = max_loss
        summary['per point sumaary']['min loss'] = min_loss
        
        
        
        return summary
        
        
        
        