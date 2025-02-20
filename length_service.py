import logging
from flask import Flask, request, jsonify
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry import trace

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Set OpenTelemetry service name
resource = Resource.create({"service.name": "length-service"})

# Initialize OpenTelemetry tracing
tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)

# Configure Jaeger Exporter (Thrift over HTTP)
jaeger_exporter = JaegerExporter(
    collector_endpoint="http://jaeger-collector.jaeger.svc.cluster.local:14268/api/traces"
)

# Add span processor
span_processor = BatchSpanProcessor(jaeger_exporter)
tracer_provider.add_span_processor(span_processor)
tracer = trace.get_tracer(__name__)

# Initialize Flask App
app = Flask(__name__)

# Instrument Flask with OpenTelemetry
FlaskInstrumentor().instrument_app(app)

@app.route('/length', methods=['POST'])
def string_length():
    with tracer.start_as_current_span("length_request") as span:
        input_data = request.get_data(as_text=True).strip()
        
        if not input_data:
            span.set_attribute("error", True)
            return jsonify({"error": "No input provided"}), 400
        
        length = len(input_data)

        # Add trace attributes
        span.set_attribute("input_length", length)

        return jsonify({"length": length})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
