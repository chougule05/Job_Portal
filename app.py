from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)


app.secret_key = 'your_secret_key'

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Vibhish@n5400',
    'database': 'job_portal',
}

USERS = {
    'admin': {'password': 'admin_password', 'role': 'admin'},
    'employer': {'password': 'employer_password', 'role': 'employer'},
    'candidate': {'password': 'candidate_password', 'role': 'candidate'},
}



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the user exists and the password is correct
        if username in USERS and USERS[username]['password'] == password:
            session['username'] = username
            session['role'] = USERS[username]['role']

            if USERS[username]['role'] == 'employer' or USERS[username]['role'] == 'admin':
                return redirect(url_for('post_job'))
            else:
                return redirect(url_for('all_jobs'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        description = request.form.get('description')
        employer = request.form.get('employer')
        email = request.form.get('email')

        with mysql.connector.connect(**DB_CONFIG) as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO jobs (title, category, description, employer, email) VALUES (%s, %s, %s, %s, %s)',
                           (title, category, description, employer, email))
            connection.commit()
        message = 'Job posted successfully!'
        return redirect(url_for('post_job'))

    return render_template('post_job.html')

@app.route('/job/<int:job_id>')
def job_details(job_id):
    with mysql.connector.connect(**DB_CONFIG) as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM jobs WHERE id = %s', (job_id,))
        job = cursor.fetchone()
    return render_template('job_details.html', job=job)


@app.route('/update_job/<int:job_id>', methods=['GET', 'POST'])
def update_job(job_id):


    with mysql.connector.connect(**DB_CONFIG) as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM jobs WHERE id = %s', (job_id,))
        job = cursor.fetchone()

    if not job:
        return 'Job not found', 404

    if request.method == 'POST':
        # Extract updated job details from the form
        updated_title = request.form.get('title')
        updated_category = request.form.get('category')
        updated_description = request.form.get('description')
        updated_employer = request.form.get('employer')
        updated_email = request.form.get('email')
        # Update the job in the database
        with mysql.connector.connect(**DB_CONFIG) as connection:
            cursor = connection.cursor()
            update_query = """
                UPDATE jobs
                SET title = %s, category = %s ,description=%s, employer = %s, email = %s
                WHERE id = %s
            """
            cursor.execute(update_query, (updated_title, updated_category, updated_description, updated_employer, updated_email, job_id))
            connection.commit()

        return redirect(url_for('all_jobs'))

    return render_template('update_job.html', job=job)


@app.route('/all_jobs')
def all_jobs():
    if 'username' not in session:
        return redirect(url_for('login'))
    with mysql.connector.connect(**DB_CONFIG) as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM jobs')
        all_jobs = cursor.fetchall()
    return render_template('all_jobs.html', all_jobs=all_jobs)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))





if __name__ == '__main__':
    app.run(debug=True)
