from flask import Flask, request, jsonify
from ml.detectionalgo import extract_colours
import logging

app = Flask(__name__)

@app.route('/analyse', methods=['POST'])
def analyse_frame():
    """ Analyse the color of a frame"""
    try:
        image_url = request.json.get('image_url')
        logging.debug(f"Loaded {image_url}")
        
        analysis_results = extract_colours(image_url)

        return jsonify({'success': True, 'results': analysis_results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
