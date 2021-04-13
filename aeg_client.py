from azure.core.credentials import AzureKeyCredential
from azure.eventgrid import EventGridPublisherClient,EventGridEvent
import os
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter



exporter = ConsoleSpanExporter()
trace.set_tracer_provider(TracerProvider(resource=Resource.create({SERVICE_NAME: "my-aeg-service"})))
tracer = trace.get_tracer(__name__)
jaeger_exporter = JaegerExporter(
    # configure agent
    agent_host_name='localhost',
    agent_port=6831,
    # optional: configure also collector
    # collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift',
    # username=xxxx, # optional
    # password=xxxx, # optional
    # max_tag_value_length=None # optional
)


trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(jaeger_exporter)
)

key = os.environ["AEG_KEY"]
endpoint = os.environ["EG_TOPIC"]
credential = AzureKeyCredential(key)

event = EventGridEvent(
    data={"team","azure-sdk"},
    subject="Door1",
    event_type="Azure.SDK.Demo",
    data_version="2.0"
)

with tracer.start_as_current_span(name="AegApplication"):
    eg_publisher_client = EventGridPublisherClient(endpoint,credential)
    print("sending event...")
    eg_publisher_client.send(event)