import sqlite3
import tyc_parse as parse
import os


class DbUtil:
    def get_conn_and_cursor(self):
        connect = sqlite3.connect('company.db')
        cursor = connect.cursor()
        return connect, cursor

    def close_cursor_conn(self, cursor, conn):
        cursor.close()
        conn.commit()
        conn.close()

    def create_company_table(self):
        conn, cursor = self.get_conn_and_cursor()

        table_sql = '''create table t_company_info (
        user_id varchar(20) primary key,
        city_name varchar(10),
        company_name varchar(100),
        company_code varchar(30),
        legal_name VARCHAR (20),
        reg_capital VARCHAR (30),
        sort_no INT,
        is_deal INT )'''
        cursor.execute(table_sql)

        self.close_cursor_conn(cursor, conn)

    def save_company_info(self, cursor, company, sort_no):
        cursor.execute('INSERT INTO t_company_info VALUES (?,?,?,?,?,?,?,?)',
                       (company['user_id'], company['city_name'], company['org_company_name'],
                        company['company_code'],
                        company['legal_name'], company['reg_capital'], sort_no, 0
                        ))

    def query_all_not_deal_company(self, cursor):
        cursor.execute('select * from t_company_info where is_deal=0 order by sort_no')
        return cursor.fetchall()

    def get_company_info_by_user_id(self, user_id, cursor):
        cursor.execute('SELECT * FROM t_company_info WHERE user_id = ?', (user_id,))
        return cursor.fetchall()

    def modify_company_info(self, company, cursor):
        update_sql = 'UPDATE t_company_info set company_code = ?,legal_name = ?,reg_capital = ?,is_deal=1 WHERE user_id = ? and is_deal = 0'
        cursor.execute(update_sql,
                       (company['company_code'], company['legal_name'], company['reg_capital'], company['user_id']))

    def query_all_company(self,cursor):
        cursor.execute('select * from t_company_info order by sort_no')
        return cursor.fetchall()


if __name__ == '__main__':
    """
     company_file_path = r'd:\第二次撞库数据.xlsx'
    company_list = exutils.read_excel(company_file_path)

    dbUtil = DbUtil()
    dbUtil.create_company_table()

    conn, cursor = dbUtil.get_conn_and_cursor()

    sort_no = 0
    for company in company_list:
        dbUtil.save_company_info(cursor, company, sort_no)
        print('插入数据：', company['user_id'], '成功')
        sort_no = sort_no + 1

    dbUtil.close_cursor_conn(cursor, conn)
    
    dbUtil = DbUtil()
    rs = dbUtil.get_company_info_by_user_id('684257576052989952')
    print(rs)
    """

    main_path_prefix = '/Users/tangjie/Downloads/companies/'
    detail_path_prefix = '/Users/tangjie/Downloads/companies/details/'

    dbUtil = DbUtil()
    conn, cursor = dbUtil.get_conn_and_cursor()

    company_no_deal_list = dbUtil.query_all_not_deal_company(cursor)
    for company_tuple in company_no_deal_list:
        company = {
            'user_id': company_tuple[0],
            'company_code': '', 'legal_name': '', 'reg_capital': ''
        }
        user_id = company_tuple[0]

        main_file_path = main_path_prefix + user_id + '.html'
        if not os.path.exists(main_file_path):
            break
        parse.parse_company(main_file_path, company)

        detail_file_path = detail_path_prefix + user_id + '.html'
        parse.parse_company_detail(detail_file_path, company)

        dbUtil.modify_company_info(company, cursor)
        print('处理完成：', company_tuple[2])

    dbUtil.close_cursor_conn(cursor, conn)
