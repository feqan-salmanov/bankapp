import string
import random
import psycopg2
from datetime import datetime
con = psycopg2.connect(
    user="postgres",
    password="feqan3.0",
    database="bank_demo",
    host="127.0.0.1",
    port="5432"
)
cursor = con.cursor()
print("""
[1] Hesab Yarat
[2] Hesaba Pul Yüklə
[3] Hesab Giriş Et
[4] Hesabdan Hesaba pul yüklə
[5] Hesab Sil
""")
secim = input("Əməliyyat Seçin :")
if secim not in ["1", "2", "3", "4", "5"]:
    raise "Belə bir prosses yoxdur."
if secim == "5":
    sil_ac = input("Account ID'si girin :")
    axc_id = f"SELECT id FROM account WHERE id=%s"
    cursor.execute(axc_id, (sil_ac))
    klm = cursor.fetchone()
    if klm is None:
        raise "Belə bir İD yoxdur.."
    else:
        sifre3 = int(input("Şifrənizi girin :"))
        sif = f"SELECT password FROM account WHERE id=%s"
        cursor.execute(sif, (sil_ac))
        sifr = cursor.fetchone()[0]
        if sifre3 == sifr:
            crt = "SELECT cteated_at FROM account_status_history WHERE account_id=%s"
            cursor.execute(crt, (sil_ac))
            crt_at = cursor.fetchone()
            time = datetime.now()
            stat = "INSERT INTO account_status_history(account_id,status_type,cteated_at,updated_at)" \
                   " VALUES(%s,%s,%s,%s) "
            cursor.execute(stat, (sil_ac, 'Passiv', crt_at, time))
            con.commit()
            print("Proses başa çatmışdır")
if secim == "1":
    print("""
    Hesab yaratmaya xoş gəlmisiniz . Zəhmət olmasa aşağıdkı məlumatları düzgün şəkildə qeyd edin.
    """)
    name = input("Ad :")
    surname = input("Soy Ad :")
    email = input("E-mail :")
    ssn = input("SSN'fin :")
    mobile = input("Mobil Telefon :")
    addres = input("Address :")
    password = int(input("Şifrə seçin :"))
    insert1 = """INSERT INTO customer(name,surname,e_mail,ssn,mobile_phone,address)
    values(%s,%s,%s,%s,%s,%s) RETURNING id"""
    cursor.execute(insert1, (name, surname, email, ssn, mobile, addres))
    customer_id = cursor.fetchone()[0]
    con.commit()
    typhe_id = random.randint(1, 2)
    insert2 = """INSERT INTO account(password,customer_id,account_type_id) VALUES(%s,%s,%s) RETURNING id"""
    cursor.execute(insert2, (password, customer_id, typhe_id))
    account_id1 = cursor.fetchone()[0]
    con.commit()
    date = datetime.now()
    insert3 = f"INSERT INTO account_status_history(cteated_at,status_type,account_id) VALUES(%s,%s,%s)"
    cursor.execute(insert3, (date, 'Active', account_id1))
    con.commit()
if secim == "2":
    id_sec = input("Account id'si yazın :")
    account_id = f"SELECT id FROM account WHERE id=%s "
    cursor.execute(account_id, (id_sec))
    data = cursor.fetchone()
    if data is None:
        raise "Belə bir İD yoxdur"
    for i in data:
        print(f"""
            Account
                Account id'si   : ---->>>> {i} 
                """)
    current_balance = f"SELECT current_balance FROM account WHERE id=%s "
    cursor.execute(current_balance, (id_sec))
    balance = cursor.fetchone()[0]
    if balance is None:
        balance = 0
    print(f"""        
                Current balance : ---->>>> {balance}
            """)
    yk_m = int(input("Yüklenecek mebleğ :"))
    if yk_m <= 0:
        raise "Səf Proses"
    balance = int(balance)
    pulum = balance + yk_m
    PRO = f"UPDATE account SET current_balance=%s WHERE id=%s"
    cursor.execute(PRO, (pulum, id_sec))
    con.commit()
    today = datetime.now()
    bf_balance = pulum - yk_m
    ctrated = "SELECT cteated_at FROM account_status_history WHERE account_id=%s"
    cursor.execute(ctrated, (id_sec))
    date = cursor.fetchone()
    abh_ab = f"INSERT INTO  account_balance_history(account_id,after_balance,before_balance" \
             f",created_at,updated_at,operation_type)"\
             f" VALUES(%s,%s,%s,%s,%s,%s)"
    cursor.execute(abh_ab, (id_sec, pulum, bf_balance, date, today, 'balans artimi'))
    con.commit()
    ASH = f"UPDATE account_status_history SET updated_at=%s WHERE account_id=%s"
    cursor.execute(ASH, (today, id_sec))
    con.commit()
    def random_char(y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))
    exxt = random_char(18)
    now = datetime.now()
    tg_id = now.strftime("%d%m%Y%H%M%S")
    ext_id = tg_id + exxt
    WORDS = ("Bank app", "Mobil_apps", "in Office")
    word = random.choice(WORDS)
    trn_id = f"INSERT INTO payments(ext_transaction_id,chanel_name,amount,account_id,created_at,updated_at)" \
             f" VALUES(%s,%s,%s,%s,%s,%s)"
    cursor.execute(trn_id, (ext_id, word, yk_m, id_sec, date, now))
    con.commit()
    ac_st_hs = f"UPDATE account_status_history SET updated_at=%s WHERE account_id=%s"
    cursor.execute(ac_st_hs, (now, id_sec))
    con.commit()
    print("PROSES BAŞA ÇATMIŞIR !!!...")
if secim == "3":
    id_sec = input("Account id'si yazın :")
    parol = int(input("Şifrənizi girin :"))
    sifre = f"SELECT password FROM account WHERE id=%s"
    cursor.execute(sifre,(id_sec))
    sifre2 = cursor.fetchone()
    passwordo = sifre2[0]
    if parol == passwordo:
        account_id = f"SELECT id,customer_id,account_type_id,current_balance FROM account WHERE id=%s "
        cursor.execute(account_id, (id_sec))
        data = cursor.fetchone()
        dira = str(data[0])
        customer = str(data[1])
        type_id = str(data[2])
        balance = str(data[3])
        if dira is None:
            raise "Belə bir İD yoxdur...."
        print(f"""
            Account
                Account id'si   : ---->>>> {dira} 
                """)
        print(f"""        
                Customer id'si  : ---->>>> {customer}    
            """)
        print(f"""        
                Account type id : ---->>>> {type_id}
            """)
        print(f"""        
                Current balance : ---->>>> {balance}
            """)
        type__ced = "SELECT account_type.id,account_type.name FROM account_type INNER JOIN account" \
                    f" ON account_type.id=account.account_type_id WHERE account.id=%s"
        cursor.execute(type__ced, (id_sec))
        tyhb = cursor.fetchone()
        typ_id = str(tyhb[0])
        typ_name = tyhb[1]
        print(f"""        
            Account Type
                Account type id : ---->>>> {typ_id}
            """)
        print(f"""        
                Account Type    : ---->>>> {typ_name}
                    """)
        account_status_history = f"SELECT account_status_history.id,account_id,status_type," \
                                 f"cteated_at,updated_at FROM account_status_history INNER JOIN account ON " \
                                 f"account.id=account_status_history.account_id WHERE account_id=%s"
        cursor.execute(account_status_history, (id_sec))
        status = cursor.fetchone()
        history = status[0]
        id_d = status[1]
        stat = status[2]
        abc = status[3]
        ate = status[4]
        print(f"""      
            ACCOUNT STATUS HISTORY
                History id        : ---->>>> {history}    
                                                         """)
        print(f"""      
                Account id        : ---->>>> {id_d}    
                                                                   """)
        print(f"""      
                Status type       : ---->>>> {stat}    
                                                       """)
        print(f"""      
                Crate at       : ---->>>> {abc}    
                                                               """)
        print(f"""      
                Update at       : ---->>>> {ate}    
                                                                       """)
        acc_bl_hs = f"SELECT account_balance_history.id,account_balance_history.account_id,before_balance," \
                    f"after_balance,created_at,account_balance_history.updated_at FROM " \
                    f"account_balance_history INNER JOIN account ON " \
                    f"account.id=account_balance_history.account_id WHERE account_id=%s "
        cursor.execute(acc_bl_hs, (id_sec))
        acblnc = cursor.fetchone()
        acb = acblnc[0]
        iner = acblnc[1]
        g = acblnc[2]
        y = acblnc[3]
        a_c = acblnc[4]
        a_e = acblnc[5]
        print(f"""     
            Account Balance History  
                A_B_H ID        : ---->>>> {acb}    
                                      """)
        print(f"""
                Account id'si   : ---->>>> {iner} 
                                           """)

        print(f"""  
                Before Balans    : ---->>>> {g}
                                                 """)

        print(f"""    
                After Balans    : ---->>>> {y}
                                                 """)
        print(f"""      
                Crate at       : ---->>>> {a_c}    
                                                                       """)
        print(f"""      
                Update at       : ---->>>> {a_e}    
                                                                               """)
        customer_id = f"SELECT customer.id,name,surname,e_mail,ssn,mobile_phone,address FROM " \
                      f"customer INNER JOIN account ON customer.id=account.customer_id " \
                      f" WHERE account.id=%s"
        cursor.execute(customer_id, (id_sec))
        customer = cursor.fetchone()
        a = customer[0]
        c_n = customer[1]
        sur = customer[2]
        em = customer[3]
        cu_ssn = customer[4]
        mobil = customer[5]
        ress = customer[6]
        print(f"""
            Customer        
               Customer id'si  : ---->>>> {a}    
                           """)
        print(f"""      
               Customer name   : ---->>>> {c_n}    
                                  """)
        print(f"""      
               Customer surname : ---->>>> {sur}    
                                          """)
        print(f"""      
               Customer E-mail  : ---->>>> {em}    
                                                  """)
        print(f"""      
               Customer SSN     : ---->>>> {cu_ssn}    
                                                          """)
        print(f"""      
               Customer Mobil-Phone     : ---->>>> {mobil}    
                                                                  """)
        print(f"""      
               Customer Address  : ---->>>> {ress}    
                                                                      """)
        payment = "SELECT payments.id,account_id,amount,chanel_name,ext_transaction_id,created_at,updated_at" \
                  f" FROM payments INNER JOIN account ON account_id=account.id WHERE account.id=%s"
        cursor.execute(payment, (id_sec))
        payments = cursor.fetchone()
        payments1 = payments[0]
        payments2 = payments[1]
        payments3 = payments[2]
        payments4 = payments[3]
        payments5 = payments[4]
        payments6 = payments[5]
        payments7 = payments[6]
        print(f"""
            Payments        
                Payment id'si  : ---->>>> {payments1}    
                                          """)
        print(f"""      
                Account id'si   : ---->>>> {payments2}    
                                                 """)
        print(f"""      
                Chanel name : ---->>>> {payments3}    
                                                         """)
        print(f"""      
                Exxt-transaction-id  : ---->>>> {payments4}    
                                                                 """)
        print(f"""      
                Amount     : ---->>>> {payments5}    
                                                                         """)
        print(f"""      
                Cerated at     : ---->>>> {payments6}    
                                                                                 """)
        print(f"""      
                Updated at  : ---->>>> {payments7}    
                                                                                     """)
    else:
        print("Şifrəni səf girmisiniz")
        raise "Şfrəni səf girmisiniz"
if secim == "4":
    vaxt = datetime.now()
    hansi_id = input("Hansı İD-dən :")
    accc_id = f"SELECT id FROM account WHERE id=%s "
    cursor.execute(accc_id, (hansi_id))
    cv_id = cursor.fetchone()
    if cv_id is None:
        print("Belə bir İD yoxdu")
        raise "Belə bir İD yoxdu"
    else:
        paasword = int(input("Şifrənizi girin :"))
        passw = f"SELECT password FROM account WHERE id=%s"
        cursor.execute(passw, (hansi_id))
        pasd = cursor.fetchone()[0]
        if paasword == pasd:
            cr_blnc = f"SELECT current_balance FROM account WHERE id=%s"
            cursor.execute(cr_blnc, (hansi_id))
            ar_cr = cursor.fetchone()[0]
            print(f"""
            Cari Balans : ----->>>  {ar_cr}
            """)
            yukl_azn = int(input("Yüklənəcək məbləğ :"))
            if yukl_azn <= 0:
                raise "Belə bir prosses yoxdur ..."
            else:
                if yukl_azn > ar_cr:
                    print("Balansda kifayət qədər vəsait yoxdur...")
                    raise "Balansda kifayət qədər vəsait yoxdur..."
                else:
                    cari_blnc = ar_cr - yukl_azn
                    before_bl = cari_blnc +yukl_azn
                    cvb_blnc = f"UPDATE account SET current_balance=%s WHERE id=%s"
                    cursor.execute(cvb_blnc, (cari_blnc, hansi_id))
                    con.commit()
                    yuk_id = int(input("Hansı İD-yə :"))
                    yuklr_id = f"SELECT id FROM account WHERE id=%s"
                    cursor.execute(yuklr_id, (yuk_id))
                    id_yuk = cursor.fetchone()[0]
                    if id_yuk is None:
                        print("Belə bir İD yoxdur")
                        raise "Belə bir İD yoxdur"
                    else:
                        yuk_crbalans = f"SELECT current_balance FROM account WHERE id=5s"
                        cursor.execute(yuk_crbalans, (yuk_id))
                        yuk_crb = cursor.fetchone()[0]
                        cr_ykblc = yukl_azn + yuk_crb
                        befor = cr_ykblc - yukl_azn
                        yuklen_id = f"UPDATE account SET current_balance=%s WHERE id=5s"
                        cursor.execute(yuklen_id, (cr_ykblc, yuk_id))
                        con.commit()
                        today = datetime.now()
                        TL = "INSERT INTO transaction_log(from_account,to_account,amount,status,created_at,updated_at)"\
                             " VALUES(%s,%s,%s,%s,%s,%s)  "
                        cursor.execute(TL, (hansi_id, yuk_id, yukl_azn, 'SUCSESS', vaxt, today))
                        con.commit()
                        abh_ab = f"INSERT INTO  account_balance_history(account_id,after_balance,before_balance" \
                                 f",created_at,updated_at,operation_type)" \
                                 f" VALUES(%s,%s,%s,%s,%s,%s)"
                        cursor.execute(abh_ab, (yuk_id, cr_ykblc, befor, vaxt, today, 'balans artimi'))
                        con.commit()
                        abh_a = f"INSERT INTO  account_balance_history(account_id,after_balance,before_balance" \
                                f",created_at,updated_at,operation_type)" \
                                f" VALUES(%s,%s,%s,%s,%s,%s)"
                        cursor.execute(abh_a, (hansi_id, cari_blnc, before_bl, vaxt, today, 'balans azalmasi'))
                        con.commit()
                        acx = "UPDATE account_status_history SET updated_at=%s WHERE account_id=%s"
                        cursor.execute(acx, (today, hansi_id))
                        con.commit()
                        acxm = "UPDATE account_status_history SET updated_at=%s WHERE account_id=%s"
                        cursor.execute(acxm, (today, yuk_id))
                        con.commit()
                        print("PROSES BAŞA ÇATMIŞIR !!!...")
        else:
            print("Səf şifrə girmisiniz...")
            raise "Səf şifrə girmisiniz..."
