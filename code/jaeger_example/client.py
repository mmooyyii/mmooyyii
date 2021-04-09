import time
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

tracer = config.initialize_tracer()

with tracer.start_span(operation_name='TestSpan') as span:
    c = {}
    s = tracer.inject(
        span_context=span.context, format='text_map', carrier=c
    )
    print(c)
    # a = requests.get('http://127.0.0.1:21111/jaeger', data={'tracer': tracer})
    # span.log_kv({'event': 'requests'})
    # print(a.text)
    # print(a.status_code)
time.sleep(2)
tracer.close()
