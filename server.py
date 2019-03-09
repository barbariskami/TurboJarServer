from flask import Flask, request, jsonify
from DataBase import DB, Rating

app = Flask(__name__)
db = DB()
table = Rating(db.conn)


@app.route('/rating', methods=['POST'])
def get_rating():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    db = DB()
    table = Rating(db.get_connection())
    table.init_table()
    if request.json['operation'] == 'get5':
        return table.return_first_5()
    elif request.json['operation'] == 'get_user':
        return table.find_user(request.json['user'])
    elif request.json['operation'] == 'post':
        table.add_user(request.json['user'], request.json['result'])


@app.route('/rating')
def show_rating():
    db = DB()
    table = Rating(db.get_connection())
    table.init_table()
    rows = table.return_all_lines()
    res = '''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width,
                        initial-scale=1, shrink-to-fit=no">
                        <link rel="stylesheet"
                        href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                        crossorigin="anonymous">
                        <title>Привет, Яндекс!</title>
                      </head>
                      <body> 
                        <table class="table">
                          <tbody>'''
    for i in range(len(rows)):
        if i == 0:
            elem = '<tr class="table-warning">'
        elif i == 1:
            elem = '<tr class="table-secondary">'
        elif i == 2:
            elem = '<tr class="table-danger">'
        else:
            elem = '<tr>'
        elem += '<td>{}</td><td>{}</td><td>{}</td>'.format(str(i + 1), rows[i][1], str(rows[i][2]))
        elem += '</tr>'
        res += elem
    res += '''</tbody>
                </table>
                </body>
                </html>'''
    return res


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
