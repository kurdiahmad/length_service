from flask import Flask, request, jsonify
import os
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry import trace

# Initialize OpenTelemetry Tracing
tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)

# Use OTLP Exporter to send traces to Jaeger
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://jaeger-collector.jaeger:4317")
otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)

# Initialize Flask App
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route('/length', methods=['POST'])
def string_length():
    input_data = request.get_data(as_text=True).strip()
    if not input_data:
        return "No input provided", 400

    return str(len(input_data))

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
