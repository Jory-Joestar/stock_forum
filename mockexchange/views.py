from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.urls import reverse
from mockexchange.models import *
from mockexchange.forms import *
from django.db.models import Q
import threading
import tushare as ts
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def index(request):
    return render(request, 'mockexchange/index.html')


# 更新总资产
def set_capital(mockuser):
    mockuser.capital = mockuser.cash
    for owned_stock in OwnedStock.objects.filter(user=mockuser):
        mockuser.capital = mockuser.capital + owned_stock.market_value
    mockuser.save()


# 第二天0点解冻当日购买股票
def unblock_lastday_balance(mockuser):
    for owned_stock in OwnedStock.objects.filter(user=mockuser):
        owned_stock.blocked_balance = owned_stock.blocked_balance - owned_stock.thisday_blocked_balance
        owned_stock.whole_balance = owned_stock.whole_balance + owned_stock.thisday_blocked_balance
        owned_stock.thisday_blocked_balance = 0
        owned_stock.save()


@login_required
def userinfo(request):
    ''' 展示用户的交易信息 '''
    # 对发送请求的用户进行操作
    testuser = UserProfile.objects.get(owner=request.user)

    set_capital(testuser)
    commission_list = testuser.commission_set.all().order_by('-index')
    deal_list = testuser.deal_set.all()
    ownedstock_list = testuser.ownedstock_set.all()
    context_dict = {'user_name': testuser.owner.username, 'user_cash': testuser.cash, 'user_capital': testuser.capital,
                    'commission_list': commission_list, 'deal_list': deal_list, 'ownedstock_list': ownedstock_list}
    return render(request, 'mockexchange/userinfo.html', context=context_dict)

@login_required
def buy(request):
    token = 'c89761557a8c339b857a2fedebea03685aee396dd2501d063d7271fd'
    ts.set_token(token)
    pro = ts.pro_api(token)
    # 获取用户
    testuser = UserProfile.objects.get(owner=request.user)

    form = CommissionForm()
    if request.method == 'POST':
        form = CommissionForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user=testuser
            new_form.name = stock_basic.select_basic_code(new_form.code, pro).name
            new_form.operation = '买入'
            # 输入序号，第1个序号为0，第2个序号为1
            commission_list = testuser.commission_set.all()
            new_form.index = len(commission_list)

            # 验证输入
            if new_form.name == 'None':
                messages.success(request,'该股票不存在')
                return render(request, 'mockexchange/buy.html', {'form': form})
            if testuser.cash < new_form.amount * new_form.price:
                messages.success(request,'资金不足')
                return render(request, 'mockexchange/buy.html', {'form': form})

            new_form.date=time.strftime("%Y%m%d", time.localtime())
            new_form.time1=time1=time.strftime("%H:%M:%S", time.localtime())
            new_form.save()

            testuser.cash = testuser.cash - new_form.amount * new_form.price
            testuser.capital = testuser.capital - new_form.amount * new_form.price
            testuser.save()
            messages.success(request,'成功创建委托')
            return render(request, 'mockexchange/buy.html', {'form': form})
        else:
            print(form.errors)
    return render(request, 'mockexchange/buy.html', {'form': form})

@login_required
def sell(request):
    token = 'c89761557a8c339b857a2fedebea03685aee396dd2501d063d7271fd'
    ts.set_token(token)
    pro = ts.pro_api(token)
    # 获取用户
    testuser = UserProfile.objects.get(owner=request.user)
    ownedstock_list = testuser.ownedstock_set.all()

    form = CommissionForm()
    if request.method == 'POST':
        form = CommissionForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user=testuser
            new_form.name = stock_basic.select_basic_code(new_form.code, pro).name
            new_form.operation = '卖出'
            # 输入序号，第1个序号为0，第2个序号为1
            commission_list = testuser.commission_set.all()
            new_form.index = len(commission_list)

            # 验证输入
            try:
                owned_stock = OwnedStock.objects.get(user=testuser, code=new_form.code)
            except:
                messages.success(request,'该股票可用余额不足')
                return render(request, 'mockexchange/sell.html', {'form': form,'ownedstock_list': ownedstock_list})
            else:
                if owned_stock.available_balance >= new_form.amount:
                    owned_stock.available_balance = owned_stock.available_balance - new_form.amount
                    owned_stock.blocked_balance = owned_stock.blocked_balance + new_form.amount
                    owned_stock.save()
                    new_form.date=time.strftime("%Y%m%d", time.localtime())
                    new_form.time1=time1=time.strftime("%H:%M:%S", time.localtime())
                    new_form.save()
                    messages.success(request,'成功创建委托')
                    return render(request, 'mockexchange/sell.html', {'form': form,'ownedstock_list': ownedstock_list})
                else:
                    messages.success(request,'该股票可用余额不足')
                    return render(request, 'mockexchange/sell.html', {'form': form,'ownedstock_list': ownedstock_list})
        else:
            print(form.errors)
    return render(request, 'mockexchange/sell.html', {'form': form,'ownedstock_list': ownedstock_list})

@login_required
def cancel(request,commission_index):
    # 获取当前用户
    testuser = UserProfile.objects.get(owner=request.user)
    commission_list = testuser.commission_set.all()

    c = Commission.objects.get(user=testuser, index=commission_index)
    if c.note != '未成交':
        messages.success(request,"该委托已成交或撤单")
    else:
        c.note = '撤单'
        c.save()
        testuser.cash = testuser.cash + c.price * c.amount
        testuser.save()
        messages.success(request,"撤单成功")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def capital_rank(request):
    capital_rank_list = UserProfile.objects.all().order_by('-capital')
    cash_rank_list = UserProfile.objects.all().order_by('-cash')
    context={'capital_rank_list':capital_rank_list,'cash_rank_list':cash_rank_list}
    return render(request,'mockexchange/capital_rank.html',context)

@login_required
def newthread(request):
    if request.user.is_superuser:
        trade = TradeThread()
        trade.start()
        return HttpResponse('开启了一个交易进程。开启之后无论这个网页是否关闭，该线程都会一直运行，直到服务器关闭。'
                        '不要重复进入这个网址，因为进入一次就会多开一个线程。暂时找不到控制线程关闭的方法。')
    else:
        raise Http404


class TradeThread(threading.Thread):
    def run(self):
        token = 'c89761557a8c339b857a2fedebea03685aee396dd2501d063d7271fd'
        ts.set_token(token)
        pro = ts.pro_api(token)

        while 1:
            if ts.get_realtime_quotes('000001').loc[0]['date'] == time.strftime("%Y-%m-%d", time.localtime()):
                current_time = int(time.strftime("%H%M%S", time.localtime()))
                if (93000 <= current_time <= 113000) or (130000 <= current_time <= 150000):
                    for commission in Commission.objects.all():
                        if commission.note == '撤单' or commission.note == '已成交':
                            continue

                        if commission.operation == '买入':
                            commission.note = '已成交'
                            commission.save()

                            new_deal = Deal(user=commission.user,
                                            date=time.strftime("%Y%m%d", time.localtime()),
                                            time1=time.strftime("%H:%M:%S", time.localtime()),
                                            code=commission.code,
                                            name=commission.name,
                                            operation='买入',
                                            amount=commission.amount,
                                            price=commission.price,
                                            poundage=0,
                                            stamp_tax=0)
                            new_deal.save()

                            try:
                                owned_stock = OwnedStock.objects.get(user=commission.user,
                                                                     code=commission.code)
                            except:
                                this_stock = stock_basic.select_basic_code(commission.code, pro)
                                ownedstock = OwnedStock(user=commission.user,
                                                        code=commission.code,
                                                        name=commission.name,
                                                        whole_balance=commission.amount,
                                                        available_balance=0,
                                                        blocked_balance=commission.amount,
                                                        thisday_blocked_balance=commission.amount,
                                                        cost=commission.price,
                                                        price=float(this_stock.get_current_price()),
                                                        profit = 0,
                                                        profit_proportion=0,
                                                        market_value=0,
                                                        whole_buy=commission.price * commission.amount,
                                                        whole_sell=0)

                                ownedstock.price = float(this_stock.get_current_price())
                                ownedstock.profit=(ownedstock.price - ownedstock.cost) * ownedstock.whole_balance
                                ownedstock.profit_proportion = (ownedstock.price - ownedstock.cost) / ownedstock.cost
                                ownedstock.market_value = ownedstock.price * ownedstock.whole_balance
                                ownedstock.save()

                                set_capital(commission.user)


                            else:
                                this_stock = stock_basic.select_basic_code(commission.code, pro)

                                owned_stock.whole_balance = owned_stock.whole_balance + commission.amount
                                owned_stock.blocked_balance = owned_stock.blocked_balance + commission.amount
                                owned_stock.thisday_blocked_balance = owned_stock.thisday_blocked_balance + commission.amount
                                owned_stock.whole_buy = owned_stock.whole_buy + commission.price * commission.amount
                                owned_stock.cost = (owned_stock.whole_buy - owned_stock.whole_sell) / owned_stock.whole_balance
                                owned_stock.price = float(this_stock.get_current_price())
                                owned_stock.profit = (owned_stock.price - owned_stock.cost) * owned_stock.whole_balance
                                owned_stock.profit_proportion = (owned_stock.price - owned_stock.cost) / owned_stock.cost
                                owned_stock.market_value = owned_stock.price * owned_stock.whole_balance
                                owned_stock.save()

                                set_capital(commission.user)

                        elif commission.operation == '卖出':
                            commission.note = '已成交'
                            commission.save()

                            this_user = commission.user
                            this_user.cash = this_user.cash + commission.price * commission.amount
                            this_user.save()

                            new_deal = Deal(user=commission.user,
                                            date=time.strftime("%Y%m%d", time.localtime()),
                                            time1=time.strftime("%H:%M:%S", time.localtime()),
                                            code=commission.code,
                                            name=commission.name,
                                            operation='卖出',
                                            amount=commission.amount,
                                            price=commission.price,
                                            poundage=0,
                                            stamp_tax=0)
                            new_deal.save()

                            this_stock = stock_basic.select_basic_code(commission.code, pro)

                            owned_stock.whole_balance = owned_stock.whole_balance + commission.amount
                            owned_stock.blocked_balance = owned_stock.blocked_balance + commission.amount
                            owned_stock.whole_sell = owned_stock.whole_sell + commission.price * commission.amount
                            owned_stock.cost = (owned_stock.whole_buy - owned_stock.whole_sell) / owned_stock.whole_balance
                            owned_stock.price = float(this_stock.get_current_price())
                            owned_stock.profit = (owned_stock.price - owned_stock.cost) * owned_stock.whole_balance
                            owned_stock.profit_proportion = (owned_stock.price - owned_stock.cost) / owned_stock.cost
                            owned_stock.market_value = owned_stock.price * owned_stock.whole_balance
                            owned_stock.save()

                            set_capital(commission.user)
            if 0 <= int(time.strftime("%H%M%S", time.localtime())) <= 30:
                for user in UserProfile.objects.all():
                    unblock_lastday_balance(user)

            time.sleep(3)
