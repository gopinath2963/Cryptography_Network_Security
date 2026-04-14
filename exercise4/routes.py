from flask import render_template, request
from . import ex4_bp
from . import md5_logic

@ex4_bp.route('/md5', methods=['GET', 'POST'])
def md5_route():
    result_hash = None
    input_text = None
    error = None
    steps = None

    if request.method == 'POST':
        try:
            input_text = request.form.get('text', '')

            # Convert string input to bytes for the algorithm
            input_bytes = input_text.encode('utf-8')

            # Call your custom MD5 function with steps
            steps = md5_logic.md5_hash_with_steps(input_bytes)
            result_hash = steps['final_hash']

        except Exception as e:
            error = f"Hashing failed: {str(e)}"

    return render_template('md5.html', result=result_hash, input_text=input_text, error=error, steps=steps)