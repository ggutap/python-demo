# coding=utf-8
import time
import re
from selenium import webdriver
from sqlalchemy import create_engine
import csv
from xlrd import open_workbook
from xlutils.copy import copy
import warnings
warnings.filterwarnings("ignore")

#导入数据到Excel中
def insert_data(data):
    # 用wlrd提供的方法读取一个excel文件
    rexcel = open_workbook("z123.xls")
    # 用wlrd提供的方法获得现在已有的行数
    rows = rexcel.sheets()[0].nrows
    # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    excel = copy(rexcel)
    # 用xlwt对象的方法获得要操作的sheet
    table = excel.get_sheet(0)
    print("<第-----" + str(rows) + "------行>\n")
    row = rows
    for value in data:
        table.write(row, 0, str(value['a_fullpath']))  # xlwt对象的写方法，参数分别是行、列、值
        table.write(row, 1, str(value['b_nickname']))
        table.write(row, 2, str(value['c_fans']))
        table.write(row, 3, str(value['d_num']))
        table.write(row, 4, str(value['e_data_time']))
        table.write(row, 5, str(value['f_from_addr']))
        table.write(row, 6, str(value['g_contents_text']))
        table.write(row, 7, str(value['h_relay']))
        table.write(row, 8, str(value['i_relay_content']))
        table.write(row, 9, str(value['j_forward']))
        table.write(row, 10, str(value['k_repeat']))
        table.write(row, 11, str(value['k_repeat']))
        table.write(row, 12, str(value['m_href']))
        table.write(row, 13, str(value['n_play_num']))
        row += 1
    # xlwt对象的保存方法，这时便覆盖掉了原来的excel
    excel.save("z123.xls")

#爬取数据
def getInfo(url):
    #打开网页并等待10秒
    driver.get(url)
    time.sleep(10)
    #滚动滑条到底部
    for i in range(1, 3):
        size = 50000 * i
        js = "var q=document.documentElement.scrollTop=" + str(size)
        driver.execute_script(js)
        #打印刷新的次数并等待5秒
        print(i)
        time.sleep(5)

    #定义数据列表
    page_info_list = []

    # 微博粉丝数
    '''
    fs_num = driver.find_elements_by_class_name("tb_counter")
    for fs in fs_num:
        tmp = fs.text.strip().split("\n")
        try:
            fans = tmp[2]
        except Exception as e:
            fans = ""
    '''
    fs_num = driver.find_elements_by_class_name("WB_frame_b")
    for fs in fs_num:
        try:
            fans = fs.find_element_by_css_selector(".tb_counter .S_line1:nth-child(2) strong").text
        except Exception as e:
            fans = "abc123"

    # 发微博的条数
    '''
    wb_num = driver.find_elements_by_class_name("WB_result")
    for wb in wb_num:
        try:
            num = wb.find_element_by_css_selector(".S_spetxt").text
        except Exception as e:
            num = ""
    '''
    wb_num = driver.find_elements_by_class_name("WB_frame_c")
    for wb in wb_num:
        try:
            num = wb.find_element_by_css_selector(".S_spetxt").text
        except Exception as e:
            print("错误提示:",e)
            num =  "0"
        finally:
            #打印获取的微博条数
            print(num)
            if int(num) >= 1:
                info0 = {}
                info0["a_fullpath"] = "fullpath"
                info0["b_nickname"] = "id"
                info0['c_fans'] = "fans"
                info0['d_num'] = "发布量"
                info0['e_data_time'] = "时间"
                info0['f_from_addr'] = "来自"
                info0["g_contents_text"] = "内容"
                info0['h_relay'] = "转发"
                info0["i_relay_content"] = "转发内"
                info0['j_forward'] = "转发"
                info0['k_repeat'] = "评价"
                info0['l_praised'] = "点赞"
                info0['m_href'] = "链接"
                info0['n_play_num'] = "播放量"
                page_info_list.append(info0)
                # contents = driver.find_elements_by_class_name("WB_feed_vipcover")
                contents = driver.find_elements_by_class_name("WB_feed_type")
                i = 1
                for content in contents:
                    try:
                        # 博主ID
                        nickname = content.find_element_by_css_selector(".WB_info a").text
                        # 时间
                        data_time = content.find_element_by_css_selector(".WB_from .S_txt2:first-child").text
                        # 来源
                        try:
                            from_addr = content.find_element_by_css_selector(".WB_from .S_txt2:nth-child(2)").text
                        except Exception as e:
                            from_addr = ""
                        emoji_pattern = re.compile(
                            u"(\ud83d[\ude00-\ude4f])|"  # emoticons
                            u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
                            u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
                            u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
                            u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
                            "+", flags=re.UNICODE)
                        # 内容
                        contents_text = content.find_element_by_css_selector(".WB_detail .WB_text").text
                        contents_text = emoji_pattern.sub(r'', contents_text)
                        # 转发
                        try:
                            relay = content.find_element_by_css_selector(".WB_expand .WB_info .W_fb").text
                        except Exception as e:
                            relay = ""
                        # 转发内
                        try:
                            relay_content = content.find_element_by_css_selector(".WB_expand .WB_text").text
                            contents_text = emoji_pattern.sub(r'', contents_text)
                        except Exception as e:
                            relay_content = ""
                        # 分享
                        forward = content.find_element_by_css_selector(".WB_handle .ficon_forward~em").text
                        # 评论
                        repeat = content.find_element_by_css_selector(".WB_handle .ficon_repeat~em").text
                        # 点赞
                        praised = content.find_element_by_css_selector(".WB_handle .ficon_praised~em").text
                        # 链接
                        try:
                            href = content.find_element_by_css_selector(".WB_from .S_txt2:first-child").get_attribute("href")
                        except Exception as e:
                            href = ""
                        info = {}
                        info["a_fullpath"] = url
                        info["b_nickname"] = nickname
                        info['c_fans'] = fans
                        info['d_num'] = num
                        info['e_data_time'] = data_time
                        info['f_from_addr'] = from_addr
                        info["g_contents_text"] = contents_text
                        info['h_relay'] = relay
                        info["i_relay_content"] = relay_content
                        info['j_forward'] = forward
                        info['k_repeat'] = repeat
                        info['l_praised'] = praised
                        info['m_href'] = href
                        info['n_play_num'] = str(i)
                        #print(info)
                        i = i + 1
                        page_info_list.append(info)
                    except Exception as e:
                        print("错误提示：", e)
                #导出
                insert_data(page_info_list)
                #df = pandas.DataFrame(page_info_list)
                '''
                try:
                    pandas.io.sql.to_sql(df, 'blog_info', yconnect, schema='spider2', if_exists='append', index=False)
                except Exception as e:
                    print("错误提示:",e)
                time.sleep(5)
                '''
            else:
                pass

#账号登录
def LoginWeibo(username, password):
    try:
        driver.get("http://login.sina.com.cn/")     #输入用户名/密码登录
        elem_user = driver.find_element_by_name("username")
        elem_user.send_keys(username)                   #用户名
        elem_pwd = driver.find_element_by_name("password")
        elem_pwd.send_keys(password)                    #密码
        elem_sub = driver.find_element_by_xpath("//input[@class='W_btn_a btn_34px']")
        elem_sub.click()                                #点击登陆因无name属性
        try:
            time.sleep(10)                              #输入验证码
            elem_sub.click() 
        except:
            pass                                        #不用输入验证码
        print(u'登陆成功...')
    except Exception as e:
        pass
    finally:
        pass

#主程序
if __name__ == "__main__":
    print(u'准备登陆Weibo.cn网站...')
    #数据库连接字段
    yconnect = create_engine('mysql://root:eline2018@123.206.210.55:3306/spider2?charset=utf8')
    #设置驱动
    driver = webdriver.Firefox(executable_path="geckodriver.exe")
    #登录微博
    LoginWeibo("13260516403@sina.cn","5262043")

    filename = "123.csv"
    url_list = csv.reader(open(filename, 'r'))
    #print(url_list)
    i = 1
    for url in url_list:
        # 访问的URL
        #url = "https://weibo.com/wynyanni?is_ori=1&is_forward=1&key_word=&start_time=2018-05-1&end_time=2018-05-31&is_search=1&is_searchadv=1"
        #getInfo(url)
        print(url[0])
        getInfo(url[0])
        print("<第------" + str(i) + "----个博主>\n")
        i += 1
        time.sleep(20)
    driver.close()


