def generate_landing_page_html():
    """
    Generates the HTML content for a landing page.
    This function returns a string containing the HTML structure for a sign-in page.
    The page includes a form with fields for email and password, styled with embedded CSS.
    Returns:
        str: A string containing the HTML content for the landing page.
    """
    landing_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign In Page</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background-image: url('https://www.proximus.be/dam/jcr:7467af79-6075-4cc2-8982-bef9f1a86cb7/cdn/sites/iportal/images/content-header/me-cor/hybrid-microsoft-teams-2407-ch/hybrid-microsoft-teams-2407-social~2024-07-04-14-13-17~cache.jpg');
            background-size: cover;
            background-position: center;
        }

        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .login-box {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
        }

        .input-group {
            margin-bottom: 15px;
        }

        .input-group label {
            display: block;
            margin-bottom: 5px;
        }

        .input-group input {
            width: 90%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #dddddd;
            border-radius: 4px;
        }

        .actions {
            text-align: center;
        }

        .button {
            background-color: #5C2D91;
            color: #ffffff;
            padding: 12px 24px;
            text-decoration: none;
            font-weight: bold;
            border-radius: 5px;
            display: inline-block;
            border: none;
            cursor: pointer;
        }

        .action {
            display: block;
            margin-top: 10px;
            color: #5C2D91;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <h1>Sign in</h1>
            <form action="/submit_form" method="post">
                <div class="input-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" placeholder="Enter email" required>
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" placeholder="Enter password" required>
                </div>
                <div class="actions">
                    <input type="submit" value="NEXT" class="button">
                    <br><br>
                    <a class="action" href="#">Can't access your account?</a>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
"""
    return landing_page
