from evolutionary_algorithm import train_population
from flask import Flask, render_template_string, send_file, request
from threading import Thread



app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <html>
    <head>
        <title>Fitness Over Generations</title>
        <script type="text/javascript">
            function refresh() {
                window.location.reload();
            }
            setInterval(refresh, 5000); // Refresh every 5 seconds
        </script>
    </head>
    <body>
        <h1>Fitness Over Generations</h1>
        <img src="/static/sheep_plot.png" alt="Sheep Fitness">
        <img src="/static/wolf_plot.png" alt="Wolves Fitness">
    </body>
    </html>
    ''')


if __name__ == '__main__':
    run_without_flask = True

    if run_without_flask:
        train_population()
    else:
        # Start the training in a separate thread
        def run_training():
            train_population()

        training_thread = Thread(target=run_training)
        training_thread.start()
        
        # Run the Flask app
        app.run(debug=True, use_reloader=False)
