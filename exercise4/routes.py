from flask import render_template, request
from . import ex4_bp
from . import md5_logic
from . import cmac_logic

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


@ex4_bp.route('/cmac', methods=['GET', 'POST'])
def cmac_route():
    result_cmac = None
    input_message = None
    input_key = None
    input_nbits = None
    error = None
    steps = None

    if request.method == 'POST':
        try:
            input_message = request.form.get('message', '')
            input_key = request.form.get('key', '')
            input_nbits = int(request.form.get('nbits', 32))

            # Call the CMAC function with steps
            steps = cmac_logic.cmac_des_with_steps(input_message, input_key, input_nbits)
            result_cmac = steps['final_cmac']

        except Exception as e:
            error = f"CMAC computation failed: {str(e)}"

    return render_template('cmac.html', result=result_cmac, input_message=input_message, input_key=input_key, input_nbits=input_nbits, error=error, steps=steps)