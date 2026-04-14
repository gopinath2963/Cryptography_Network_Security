# exercise1/routes.py
from flask import render_template, request, redirect, url_for
from . import ex1_bp  # Import the blueprint we created in __init__.py

# Import your modules using relative imports (from . import ...)
from . import affine_cipher
from . import playfair_cipher
from . import vigenere_cipher
from . import fermat_theorem
from . import crypto_utils

# --- Routes ---

# Note: We don't need the '/' root route here, that stays in the main app.py

@ex1_bp.route('/affine', methods=['GET', 'POST'])
def affine_route():
    result, error, mode, steps = None, None, None, None
    if request.method == 'POST':
        try:
            pt = request.form.get('text', '')
            a = request.form.get('a', '')
            b = request.form.get('b', '')

            if 'encrypt' in request.form:
                result, steps = affine_cipher.encrypt_affine(pt, a, b)
                mode = "Ciphertext"
            elif 'decrypt' in request.form:
                result, steps = affine_cipher.decrypt_affine(pt, a, b)
                mode = "Plaintext"
        except Exception as e: error = str(e)
    return render_template('affine.html', result=result, error=error, mode=mode, steps=steps)

@ex1_bp.route('/playfair', methods=['GET', 'POST'])
def playfair_route():
    data, error, mode = None, None, None
    if request.method == 'POST':
        try:
            text = request.form.get('text', '')
            key = request.form.get('key', '')
            
            if 'encrypt' in request.form:
                data = playfair_cipher.playfair_process(text, key, 'encrypt')
                mode = "Encryption"
            elif 'decrypt' in request.form:
                data = playfair_cipher.playfair_process(text, key, 'decrypt')
                mode = "Decryption"
        except Exception as e: error = str(e)
    return render_template('playfair.html', data=data, error=error, mode=mode)

@ex1_bp.route('/hill_math', methods=['GET', 'POST'])
def hill_math_route():
    gcd_val, linear_combo, steps, error, mode = None, None, None, None, None
    a_val, b_val, calc_a, calc_b = None, None, None, None

    if request.method == 'POST':
        try:
            a_str = request.form.get('a')
            b_str = request.form.get('b')
            action = request.form.get('action') 

            if not a_str or not b_str: raise ValueError("Please enter both numbers.")
            a = int(a_str)
            b = int(b_str)
            a_val, b_val = a, b
            
            swapped = False
            if b > a:
                calc_a, calc_b = b, a
                swapped = True
            else:
                calc_a, calc_b = a, b
                swapped = False

            g, x, y, calc_steps = crypto_utils.extended_gcd_verbose(calc_a, calc_b)
            gcd_val = g
            steps = calc_steps

            if action == 'gcd':
                mode = 'gcd'
            elif action == 'extended':
                mode = 'extended'
                if swapped: coeff_a, coeff_b = y, x
                else: coeff_a, coeff_b = x, y
                op = "+" if coeff_b >= 0 else "-"
                linear_combo = f"{a_val}({coeff_a}) {op} {b_val}({abs(coeff_b)}) = {g}"

        except Exception as e: error = str(e)
        
    return render_template('hill_math.html', gcd=gcd_val, steps=steps, linear_combo=linear_combo, error=error, a_val=a_val, b_val=b_val, calc_a=calc_a, calc_b=calc_b, mode=mode)

@ex1_bp.route('/vigenere', methods=['GET', 'POST'])
def vigenere_route():
    result, error, mode, steps = None, None, None, None
    if request.method == 'POST':
        try:
            text = request.form.get('text', '')
            key = request.form.get('key', '')

            if 'encrypt' in request.form:
                result, steps = vigenere_cipher.encrypt_vigenere(text, key)
                mode = "Ciphertext"
            elif 'decrypt' in request.form:
                result, steps = vigenere_cipher.decrypt_vigenere(text, key)
                mode = "Plaintext"
        except Exception as e: error = str(e)
    return render_template('vigenere.html', result=result, error=error, mode=mode, steps=steps)

@ex1_bp.route('/fermat', methods=['GET', 'POST'])
def fermat_route():
    result, error, steps = None, None, None
    if request.method == 'POST':
        try:
            action = request.form.get('action', 'primality')

            if action == 'primality':
                n_str = request.form.get('n')
                if not n_str: raise ValueError("Please enter a number.")
                n = int(n_str)
                is_prime, step_list = fermat_theorem.is_prime_fermat(n)
                result = f"{n} is {'prime' if is_prime else 'composite'}"
                steps = step_list

            elif action == 'theorem':
                a_str = request.form.get('a')
                p_str = request.form.get('p')
                if not a_str or not p_str: raise ValueError("Please enter both a and p.")
                a = int(a_str)
                p = int(p_str)
                holds, step_list = fermat_theorem.fermat_little_theorem_demo(a, p)
                if holds is None:
                    result = step_list  # Error message
                else:
                    result = f"Fermat's Little Theorem {'holds' if holds else 'does not hold'} for a={a}, p={p}"
                steps = step_list if holds is not None else None

        except Exception as e: error = str(e)
    return render_template('fermat.html', result=result, error=error, steps=steps)