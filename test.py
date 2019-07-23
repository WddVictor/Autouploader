from operations import *
import csv


def resolve_name_md5():
    global name_md5_con
    name_md5_con = read_report(os.path.join(reports_path, 'name_md5_correspondence.csv'), read_by_name=True)


if __name__ == '__main__':
    resolve_name_md5()

    md5_csv_path = os.path.join(md5_path, 'md5.csv')
    to_write = dict({})
    report_data = read_report(report_csv_path(1))
    app_2_md5 = read_md5(md5_csv_path)
    md5_2_app = read_md5(md5_csv_path, True)
    app_name_con = dict({})
    report_header = ['app', 'report']
    for md5 in name_md5_con.keys():
        if md5 in md5_2_app.keys():
            name = name_md5_con[md5]
            app = md5_2_app[md5]
            app_name_con[name] = app
            app_name_con[app] = name
            to_write[app] = report_data[name]

    with open(report_csv_path(1), "w", encoding='utf8', newline='') as out_report:
        report_writer = csv.DictWriter(out_report, report_header)
        report_writer.writeheader()
        report_writer.writerows(dict_to_csv(to_write, 'app', 'report'))
