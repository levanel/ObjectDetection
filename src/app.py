from flask import Flask, request, jsonify, send_file
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/submit-attention', methods=['POST'])
def receive_data():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400

    try:
        # Extract info from request
        object_durations = data.get('objectDurations', {})
        total_time = data.get('totalTime', 0)
        phone_time = data.get('phoneTime', 0)
        attention_percentage = data.get('attentionPercentage', 0)
        total_attention_in_class = data.get('totalAttentionInClass', 0)

        # Create DataFrame
        df = pd.DataFrame([
            {'Object Type': obj, 'Duration (s)': duration}
            for obj, duration in object_durations.items()
        ])

        # Add summary rows
        df = df.append({
            'Object Type': 'TOTAL TIME',
            'Duration (s)': total_time
        }, ignore_index=True)

        df = df.append({
            'Object Type': 'PHONE TIME',
            'Duration (s)': phone_time
        }, ignore_index=True)

        df = df.append({
            'Object Type': 'TOTAL ATTENTION (seconds)',
            'Duration (s)': total_attention_in_class
        }, ignore_index=True)

        df = df.append({
            'Object Type': 'TOTAL ATTENTION (%)',
            'Duration (s)': attention_percentage
        }, ignore_index=True)

        # Save to Excel
        filename = f"attention_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join('reports', filename)
        os.makedirs('reports', exist_ok=True)
        df.to_excel(filepath, index=False)

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
