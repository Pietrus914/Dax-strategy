import csv

DATA = []
GODZ = []
OTWARCIE = []
MINIMUM = []
MAXIMUM = []
ZAMKNIECIE = []
STREFY_LISTA = []
list_up = []
list_down = []
BOX_SIZE = []
TP_CLOSE_POSITION = []
SL_CLOSE_POSITION = []
TP_CLOSE_POSITION_SELL = []
SL_CLOSE_POSITION_SELL = []
count_buy_list = []
count_sell_list = []
all_list = []
buy_list = []
sell_list = []
reward = int(input("Chose your R:R level, enter reward: "))
risk = int(input("Chose your R:R level, enter risk: "))

path = '[DAX30]5.csv'

def column():

  with open(path, 'r') as csvfile:

    for line in csvfile:
      fields = line.split(",")
      data = fields[0]
      DATA.append(data)
      godz = str(fields[1])
      GODZ.append(godz)
      otwarcie = float(fields[2])
      otwarcie = round(otwarcie,4)
      OTWARCIE.append(otwarcie)
      minimum = float(fields[4])
      MINIMUM.append(minimum)
      maximum = float(fields[3])
      MAXIMUM.append(maximum)
      zamkniecie = float(fields[5])
      ZAMKNIECIE.append(zamkniecie)

  #  for i in range(len(DATA)):
  #    
  #    print(f"{DATA[i]} | {GODZ[i]} | {OTWARCIE[i]}   |   {MAXIMUM[i]} | {MINIMUM[i]} | {ZAMKNIECIE[i]} ".format(" {:^10} "))
  #print()
  
  return DATA, GODZ, OTWARCIE, MAXIMUM,MINIMUM, ZAMKNIECIE

#column()

def get_input(text):
    user_input=input(text)
    return user_input


def box(DATA, GODZ, OTWARCIE, MAXIMUM, MINIMUM, ZAMKNIECIE):
    chose_time = get_input("Wybierz godzinę: ")
    list1=[]
    
    #utworzenie listy z wielkościami boxów w wyznaczonej godzinie
    for i in range(len(DATA)-1):
          
        if GODZ[i] == chose_time:
            box = round((MAXIMUM[i] - MINIMUM[i]),2)
            BOX_SIZE.append(box)
            list1.append([DATA[i], GODZ[i], OTWARCIE[i], MAXIMUM[i],MINIMUM[i], ZAMKNIECIE[i]])
    #print(BOX_SIZE)
    print(len(BOX_SIZE))

    #ustalenie czy box został wybity górą czy dołem, dodanie wyników do poszczególnych list
    for j in range(len(list1)):
          
        for k in range(len(OTWARCIE)):
              
            if list1[j][2] == OTWARCIE[k]:
                  
                for l in range(k+1, len(OTWARCIE)):
                      
                    if list1[j][3] < OTWARCIE[l]:
                        #print('wyjście górą',DATA[l], GODZ[l], OTWARCIE[l])
                        list_up.append([DATA[l], GODZ[l], OTWARCIE[l]] )
                        break
                        
                    elif list1[j][4] > OTWARCIE[l]:
                        #print("wyjście dołem",DATA[l], GODZ[l], OTWARCIE[l])
                        list_down.append([DATA[l], GODZ[l], OTWARCIE[l]])
                        break
    #print(len(list_up), list_up)
    return list_up, list_down, BOX_SIZE

#print(box(DATA, GODZ, OTWARCIE, MAXIMUM,MINIMUM, ZAMKNIECIE))

def tp_sl_buy(list_up, BOX_SIZE, DATA, GODZ, OTWARCIE, MAXIMUM, MINIMUM):
    data_list_up = 0
    open_list_up = 2
    #reward = 3
    #risk = 2
    
    for i in range(len(list_up)):
        
        for j in range(len(MAXIMUM)):
              
            if list_up[i][data_list_up] == DATA[j] and list_up[i][open_list_up] == OTWARCIE[j]:
                  
                  for k in range(j+1, len(MAXIMUM)):
                        win_level = list_up[i][open_list_up] + (BOX_SIZE[i] * reward)
                        
                        if MAXIMUM[k] > win_level:
                            TP_CLOSE_POSITION.append([DATA[k], GODZ[k], MAXIMUM[k]])
                            break

                  for l in range(j+1, len(MINIMUM)): 
                        lost_level = list_up[i][open_list_up] - (BOX_SIZE[i] * risk)     
                        if MINIMUM[l] < lost_level:
                            SL_CLOSE_POSITION.append([DATA[l], GODZ[l], MINIMUM[l]])
                            break
    #print(BOX_SIZE)
    #print(SL_CLOSE_POSITION)
    #print(len(SL_CLOSE_POSITION))
    #print(TP_CLOSE_POSITION)
    #print(len(TP_CLOSE_POSITION))
    data_close = 0
    time_close = 1
    count_tp = 0
    count_sl = 0

    #sprawdzamy który poziom był osiągniągnięty jako pierwszy (SL czy TP), zliczamy ilości
    for i in range(len(SL_CLOSE_POSITION)):
        
            if TP_CLOSE_POSITION[i][data_close] < SL_CLOSE_POSITION[i][data_close] or (TP_CLOSE_POSITION[i][data_close] == SL_CLOSE_POSITION[i][data_close] and TP_CLOSE_POSITION[i][time_close] < SL_CLOSE_POSITION[i][data_close]):
                  count_tp += 1
            else:
                  count_sl +=1

    #print(len(TP_CLOSE_POSITION))
    #print(len(SL_CLOSE_POSITION))
    #print(count_tp)
    #print(count_sl)   
    count_buy_list.append([count_tp, count_sl])
                   
    return count_buy_list

#print(tp_sl_buy(list_up, BOX_SIZE, DATA, GODZ, OTWARCIE, MAXIMUM, MINIMUM))

def tp_sl_sell(list_down, BOX_SIZE, DATA, GODZ, OTWARCIE, MAXIMUM, MINIMUM):
    data_list_down = 0
    open_list_down = 2
    count_tp_sell = 0
    count_sl_sell = 0
    #reward = 3
    #risk = 2
    for i in range(len(list_down)):
          
        for j in range(len(MINIMUM)):
              
            if list_down[i][data_list_down] == DATA[j] and list_down[i][open_list_down] == OTWARCIE[j]:
                  
                  for k in range(j+1, len(MINIMUM)):
                        win_level = list_down[i][open_list_down] - (BOX_SIZE[i] * reward)
                        

                        if MINIMUM[k] < win_level:
                            TP_CLOSE_POSITION_SELL.append([DATA[k], GODZ[k], MAXIMUM[k]])
                            break

                  for l in range(j+1, len(MAXIMUM)): 
                        lost_level = list_down[i][open_list_down] + (BOX_SIZE[i] * risk)     
                        if MAXIMUM[l] > lost_level:
                            SL_CLOSE_POSITION_SELL.append([DATA[l], GODZ[l], MINIMUM[l]])
                            break

    #print(len(TP_CLOSE_POSITION_SELL))
    #print(len(SL_CLOSE_POSITION_SELL))
    data_close = 0
    time_close = 1

    #sprawdzamy który poziom był osiągniągnięty jako pierwszy (SL czy TP), zliczamy ilości
    for i in range(len(TP_CLOSE_POSITION_SELL)):

        if TP_CLOSE_POSITION_SELL[i][data_close] < SL_CLOSE_POSITION_SELL[i][data_close] or (TP_CLOSE_POSITION_SELL[i][data_close] == SL_CLOSE_POSITION_SELL[i][data_close] and TP_CLOSE_POSITION_SELL[i][time_close] < SL_CLOSE_POSITION_SELL[i][data_close]):
              count_tp_sell += 1
        else:
              count_sl_sell +=1

    count_sell_list.append([count_tp_sell, count_sl_sell])
    
    return count_sell_list

#tp_sl_sell(list_down, BOX_SIZE, DATA, GODZ, OTWARCIE, MAXIMUM, MINIMUM)

def win_lost_statistic(count_buy_list, count_sell_list):
    
    one_list_elem = 0
    win = 0
    lost = 1

    for i in range(len(count_buy_list)):
        
        all_win = count_buy_list[one_list_elem][win] + count_sell_list[one_list_elem][win]
        all_lost = count_buy_list[one_list_elem][lost] + count_sell_list[one_list_elem][lost]
        all_positions = all_win + all_lost
        effectiveness = round((all_win / all_positions * 100), 2)
        all_list.append([all_win, all_lost, effectiveness, all_positions])

        win_buy = count_buy_list[one_list_elem][win]
        lost_buy = count_buy_list[one_list_elem][lost]
        all_buy = count_buy_list[one_list_elem][win] + count_buy_list[one_list_elem][lost]
        effectiveness_buy = round((win_buy / all_buy * 100), 2)
        buy_list.append([win_buy, lost_buy, effectiveness_buy, all_buy])

        win_sell = count_sell_list[one_list_elem][win]
        lost_sell = count_sell_list[one_list_elem][lost]
        all_sell = count_sell_list[one_list_elem][win] + count_sell_list[one_list_elem][lost]
        effectiveness_sell = round((win_sell / all_sell * 100), 2)
        sell_list.append([win_sell, lost_sell, effectiveness_sell, all_sell])

    return sum(all_list, []), sum(buy_list, []), sum(sell_list, [])


def print_stat(all_list, buy_list, sell_list):
    first_elem = 0
    wins = 0
    lost = 1
    effect = 2
    all_enters = 3
    saldo = int(get_input('Enter your max loss in dollars for one invest: '))
    wins_money = saldo * all_list[first_elem][wins] * reward
    lost_money = saldo * all_list[first_elem][lost] * risk
    bilans = wins_money - lost_money

    print()
    print("/------------------------------------------------------------------------------------------------------------------------------------\\")
    print(f"|  ALL POSITION                    - {all_list[first_elem][all_enters]}     |  BUY POSITION                    - {buy_list[first_elem][all_enters]}     |  SELL POSITION                    - {sell_list[first_elem][all_enters]}     |")
    print("|-------------------------------------------|-------------------------------------------|--------------------------------------------|")
    print(f"|  ALL WINS POSITION               - {all_list[first_elem][wins]}     |  BUY WINS POSITION               - {buy_list[first_elem][wins]}     |  SELL WINS POSITION               - {sell_list[first_elem][wins]}      |")
    print("|-------------------------------------------|-------------------------------------------|--------------------------------------------|")
    print(f"|  ALL LOST POSITION               - {all_list[first_elem][lost]}     |  BUY LOST POSITION               - {buy_list[first_elem][lost]}     |  SELL LOST POSITION               - {sell_list[first_elem][lost]}     |")
    print("|-------------------------------------------|-------------------------------------------|--------------------------------------------|")
    print(f"|  EFFECTIVENESS OF THE STRATEGY   - {all_list[first_elem][effect]}% |  EFFECTIVENESS OF BUY POSITION   - {all_list[first_elem][effect]}% |  EFFECTIVENESS OF SELL POSITION   - {sell_list[first_elem][effect]}% |")
    print("\------------------------------------------------------------------------------------------------------------------------------------/")
    print("/---------------------------------|")
    print("|  {:10}        = {:^10} |".format("MAX RISK",saldo))
    print("|  {:10}    = {:^10} |".format('ALL WINS MONEY', wins_money))
    print("|  {:10}    = {:^10} |".format('ALL LOST MONEY', lost_money))
    print("|  {:10}        = {:^10} |".format('BILANS',bilans))
    print("\\---------------------------------/")
    pass

def main():
    column()
    
    
    box(DATA, GODZ, OTWARCIE, MAXIMUM, MINIMUM, ZAMKNIECIE)
    tp_sl_buy(list_up, BOX_SIZE, DATA, GODZ, OTWARCIE, MAXIMUM, MINIMUM)
    tp_sl_sell(list_down, BOX_SIZE, DATA, GODZ, OTWARCIE, MAXIMUM, MINIMUM)
    win_lost_statistic(count_buy_list, count_sell_list)
    print_stat(all_list, buy_list, sell_list)
    

main()
