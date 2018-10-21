import os.path
import numpy as np

from flask import Flask, Response
import json
import randscanner as ras
import random as rad

app = Flask(__name__)
app.config.from_object(__name__)


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

old_min = -1
old_max = -1
s_history = np.empty(0);
d_history = np.empty(0);

@app.route('/random/<range_min>/<range_max>', methods=['GET'])
def random(range_min, range_max):  # pragma: no cover

    global old_min;
    global old_max;
    global s_history;
    global d_history;

    rs = (ras.random()*(int(range_max)-int(range_min)))+int(range_min),
    rd = (rad.random()*(int(range_max)-int(range_min)))+int(range_min)

    if range_min != old_min or range_max != old_max:
        s_history = np.empty(0);
        d_history = np.empty(0);

    s_history = np.append(s_history, rs)
    d_history = np.append(d_history, rd)

    custcorr = np.correlate(s_history, s_history, "same")
    normcorr = np.correlate(d_history, d_history, "same")
    # use only second half
    custcorr = custcorr[int(len(custcorr)/2):]
    normcorr = normcorr[int(len(normcorr)/2):]
 
    old_min = range_min;
    old_max = range_max;

    data = {
        "rd": rd,
        "rs": rs,
        "aus": custcorr.tolist(),
        "aud": normcorr.tolist()
    }

    return Response(json.dumps(data), status=200, mimetype="application/json")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)


if __name__ == '__main__':  # pragma: no cover
    app.run(port=80)
