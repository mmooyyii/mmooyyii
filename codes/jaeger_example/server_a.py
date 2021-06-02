from flask import Flask, request
import requests

import logging
from jaeger_client import Config

log_level = logging.DEBUG
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)

config = Config(
    config={'sampler': {'type': 'const', 'param': 1}},
    service_name='jaeger_example2',
    validate=True,
)
app = Flask(__name__)


@app.route('/jaeger')
def hello_world():
    tracer = request.form['tracer']
    print(tracer)
    with tracer.start_span(operation_name='TestSpan') as span:
        span.log_kv({'event': 'server_a'})
        return "123"


if __name__ == '__main__':
    app.run(port=21111)
