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
    axc_id = f"SELECT id FROM account WHERE id={sil_ac}"
    cursor.execute(axc_id)
    klm = cursor.fetchone()
    if klm is None:
        raise "Belə bir İD yoxdur.."
    else:
        sifre3 = int(input("Şifrənizi girin :"))
        sif = f"SELECT password FROM account WHERE id={sil_ac}"
        cursor.execute(sif)
        sifr = cursor.fetchone()[0]
        if sifre3 == sifr:
            silinen_hes = f"DELETE FROM account WHERE id={sil_ac}"
            cursor.execute(silinen_hes)
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
    insert1 = """INSERT INTO customer(name,surmane,e_mail,ssn,mobil_phone,address)
    values(%s,%s,%s,%s,%s,%s) RETURNING id"""
    cursor.execute(insert1, (name, surname, email, ssn, mobile, addres))
    customer_id = cursor.fetchone()[0]
    con.commit()
    print("""
       Hesab növü seçin
             [1] Private
             [2] Corparate
       """)
    typhe = input("Hesab növü :")
    if typhe not in ["1", "2"]:
        raise " Belə bir secim yoxdur"
    if typhe == "1":
        typ = "INSERT INTO account_type(name) VALUES('Private') RETURNING id"
        cursor.execute(typ)
        con.commit()
        typhe_id = cursor.fetchone()[0]
        insert2 = """INSERT INTO account(password,customer_id,account_type_id) VALUES(%s,%s,%s)"""
        cursor.execute(insert2, (password, customer_id, typhe_id))
    if typhe == "2":
        typhd = """INSERT INTO account_type(name) VALUES('Corparate') RETURNING id"""
        cursor.execute(typhd)
        con.commit()
        typhe_id2 = cursor.fetchone()[0]
        insert2 = """INSERT INTO account(password,customer_id,account_type_id) VALUES(%s,%s,%s)"""
        cursor.execute(insert2, (password, customer_id, typhe_id2))
        con.commit()
    date = datetime.now()
    insert3 = f"INSERT INTO account_status_history(created_at) VALUES('{date}')"
    cursor.execute(insert3)
    con.commit()
    insert4 = f"INSERT INTO transaction_log(crated_at) VALUES('{date}')"
    cursor.execute(insert4)
    con.commit()
    insert5 = f"INSERT INTO account_balance_history(crated_at) VALUES('{date}')"
    cursor.execute(insert5)
    con.commit()
    insert6 = f"INSERT INTO payments(crated_at) VALUES('{date}')"
    cursor.execute(insert6)
    con.commit()
if secim == "2":
    id_sec = input("Account id'si yazın :")
    account_id = f"SELECT id FROM account WHERE id={id_sec} "
    cursor.execute(account_id)
    data = cursor.fetchone()
    if data is None:
        raise "Belə bir İD yoxdur"
    for i in data:
        print(f"""
            Account
                Account id'si   : ---->>>> {i} 
                """)
    current_balance = f"SELECT current_balance FROM account WHERE id={id_sec} "
    cursor.execute(current_balance)
    balance = cursor.fetchone()
    for c in balance:
        print(f"""        
                Current balance : ---->>>> {c}
            """)
    yk_m = int(input("Yüklenecek mebleğ :"))
    if yk_m <= 0:
        raise "Səf Proses"
    balance = balance[0]
    pulum = balance + yk_m
    PRO = f"UPDATE account SET current_balance={pulum} WHERE id={id_sec}"
    cursor.execute(PRO)
    con.commit()
    today = datetime.now()
    bf_balance = pulum - yk_m
    abh_ab = f"UPDATE account_balance_history SET after_balance=%s, before_balance=%s, updated_at=%s " \
             f"WHERE account_id={id_sec}"
    cursor.execute(abh_ab, (pulum, bf_balance, today))
    con.commit()
    ASH = f"UPDATE account_status_history SET updated_at={today} WHERE account_id={id_sec}"
    cursor.execute(ASH)
    con.commit()
    TL = f"UPDATE transaction_log SET updated_at={today} WHERE from_account={id_sec}"
    cursor.execute(TL)
    con.commit()
    PAY = f"UPDATE payments SET updated_at={today} WHERE account.id={id_sec}"
    cursor.execute(PAY)
    con.commit()
    TL_in = f"UPDATE payments SET amount={yk_m} WHERE account_id={id_sec}"
    cursor.execute(TL_in)
    con.commit()
    def random_char(y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))
    exxt = random_char(18)
    now = datetime.now()
    tg_id = now.strftime("%d%m%Y%H%M%S")
    ext_id = exxt + tg_id
    trn_id = f"INSERT INTO payments(exxt_transaction_id) VALUES({ext_id} WHERE account_id={id_sec})"
    cursor.execute(trn_id)
    con.commit()
    WORDS = ("Bank app", "Mobil_apps", "in Office")
    word = random.choice(WORDS)
    ch_name = f"INSERT INTO payments(chanel_name) VALUES({word} WHERE account_id={id_sec})"
    cursor.execute(ch_name)
    con.commit()
    print("PROSES BAŞA ÇATMIŞIR !!!...")
if secim == "3":
    id_sec = int(input("Account id'si yazın :"))
    parol = int(input("Şifrənizi girin :"))
    sifre = f"SELECT password FROM account WHERE id={id_sec}"
    cursor.execute(sifre)
    sifre2 = cursor.fetchone()
    passwordo = sifre2[0]
    if parol == passwordo:
        account_id = f"SELECT id,customer_id,account_type_id,current_balance FROM account WHERE id={id_sec} "
        cursor.execute(account_id)
        data = cursor.fetchone()
        dira = str(data[0])
        customer = str(data[1])
        type_id = str(data[2])
        balance = str(data[3])
        if dira is None:
            raise "Belə bir İD yoxdur...."
        for i in dira:
            print(f"""
            Account
                Account id'si   : ---->>>> {i} 
                """)
        for a in customer:
            print(f"""        
                Customer id'si  : ---->>>> {a}    
            """)
        for b in type_id:
            print(f"""        
                Account type id : ---->>>> {b}
            """)
        for c in balance:
            print(f"""        
                Current balance : ---->>>> {c}
            """)
        type__ced = "SELECT account_type.id,account_type.name FROM account_type INNER JOIN account" \
                    f" ON account_type.id=account.account_type_id WHERE account.id={id_sec}"
        cursor.execute(type__ced)
        tyhb = cursor.fetchone()
        typ_id = str(tyhb[0])
        typ_name = tyhb[1]
        for b in typ_id:
            print(f"""        
            Account Type
                Account type id : ---->>>> {b}
            """)
            print(f"""        
                Account Type    : ---->>>> {typ_name}
                    """)
        account_status_history = f"SELECT account_status_history.id,account_id,status_type," \
                                 f"created_at,updated_at FROM account_status_history INNER JOIN account ON " \
                                 f"account.id=account_status_history.account_id WHERE account_id={id_sec}"
        cursor.execute(account_status_history)
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
                    f"account.id=account_balance_history.account_id WHERE account_id={id_sec} "
        cursor.execute(acc_bl_hs)
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
        customer_id = f"SELECT customer.id,name,surmane,e_mail,ssn,mobil_phone,address FROM " \
                      f"customer INNER JOIN account ON customer.id=account.customer_id " \
                      f" WHERE account.id={id_sec}"
        cursor.execute(customer_id)
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
        tr_log = "SELECT transaction_log.id,from_account,to_account,amount,status,created_at,updated_at " \
                 f"FROM transaction_log INNER JOIN account ON from_account=account.id WHERE account.id={id_sec}"
        cursor.execute(tr_log)
        trans_log = cursor.fetchone()
        trans1 = trans_log[0]
        trans2 = trans_log[1]
        trans3 = trans_log[2]
        trans4 = trans_log[3]
        trans5 = trans_log[4]
        trans6 = trans_log[5]
        trans7 = trans_log[6]
        print(f"""
            Transactin log        
               Transaction id'si  : ---->>>> {trans1}    
                                  """)
        print(f"""      
               From account   : ---->>>> {trans2}    
                                         """)
        print(f"""      
               To account : ---->>>> {trans3}    
                                                 """)
        print(f"""      
               Amount  : ---->>>> {trans4}    
                                                         """)
        print(f"""      
               Status     : ---->>>> {trans5}    
                                                                 """)
        print(f"""      
               Cerated at     : ---->>>> {trans6}    
                                                                         """)
        print(f"""      
               Updated at  : ---->>>> {trans7}    
                                                                             """)
        payment = "SELECT payments.id,account_id,amount,chanel_name,exxt_transaction_id,created_at,updated_at" \
                  f" FROM payments INNER JOIN account ON account_id=account.id WHERE account.id={id_sec}"
        cursor.execute(payment)
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
    hansi_id = input("Hansı İD-dən :")
    accc_id = f"SELECT id FROM account WHERE id={hansi_id} "
    cursor.execute(accc_id)
    cv_id = cursor.fetchone()
    if cv_id is None:
        print("Belə bir İD yoxdu")
        raise "Belə bir İD yoxdu"
    else:
        paasword = int(input("Şifrənizi girin :"))
        passw = f"SELECT password FROM account WHERE id={hansi_id}"
        cursor.execute(passw)
        pasd = cursor.fetchone()[0]
        if paasword == pasd:
            cr_blnc = f"SELECT current_balance FROM account WHERE id={hansi_id}"
            cursor.execute(cr_blnc)
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
                    cvb_blnc = f"UPDATE account SET current_balance={cari_blnc} WHERE id={hansi_id}"
                    cursor.execute(cvb_blnc)
                    con.commit()
                    yuk_id = int(input("Hansı İD-yə :"))
                    yuklr_id = f"SELECT id FROM account WHERE id={yuk_id}"
                    cursor.execute(yuklr_id)
                    id_yuk = cursor.fetchone()[0]
                    if id_yuk is None:
                        print("Belə bir İD yoxdur")
                        raise "Belə bir İD yoxdur"
                    else:
                        yuk_crbalans = f"SELECT current_balance FROM account WHERE id={yuk_id}"
                        cursor.execute(yuk_crbalans)
                        yuk_crb = cursor.fetchone()[0]
                        cr_ykblc = yukl_azn + yuk_crb
                        yuklen_id = f"UPDATE account SET current_balance={cr_ykblc} WHERE id={yuk_id}"
                        cursor.execute(yuklen_id)
                        con.commit()
                        today = datetime.now()
                        TL = f"INSERT INTO transaction_log(updated_at) VALUES={today}  "
                        cursor.execute(TL)
                        con.commit()
                        ABH = f"INSERT INTO account_balance_history(updated_at) VALUES={today} "
                        cursor.execute(ABH)
                        con.commit()
                        bh = "UPDATE account_balance_history SET before_balance=%s, after_balance=%s," \
                             " operation_type=%s " \
                             f"WHERE account_id={yuk_id}"
                        cursor.execute(bh, (yuk_crb, yukl_azn, 'Pul Yukleme'))
                        con.commit()
                        TL_in = f"UPDATE transaction_log SET amount={yukl_azn} WHERE from_account={hansi_id}," \
                                f"to_account{yuk_id}"
                        print("PROSES BAŞA ÇATMIŞIR !!!...")
                    insert20 = f"UPDATE transaction_log SET to_account={yuk_id} WHERE from_account={hansi_id}"
                    cursor.execute(insert20)
                    con.commit()
        else:
            print("Səf şifrə girmisiniz...")
            raise "Səf şifrə girmisiniz..."
