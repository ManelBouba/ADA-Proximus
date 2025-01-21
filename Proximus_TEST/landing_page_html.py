def generate_landing_page_html():
    """
    Generates the HTML for the landing page with a form.
    """
    landing_page = """
    <html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Email Template</title>
	<style type="text/css">body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .email-container {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border: 1px solid #dddddd;
            border-radius: 8px;
            overflow: hidden;
        }
        .rs-border-c2 {
            border: 3px solid #5C2D91;
            padding: 20px;
        }
        .email-header {
            text-align: center;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .email-header img {
            max-width: 150px;
            height: auto;
        }
        .email-body {
            padding: 30px; /* Increased padding inside the body */
            color: #333333;
            text-align: left;
            height: 300px; /* Increased height for more space */
            overflow: hidden;
        }
        .button-container {
            text-align: center;
            margin-top: 30px; /* Added more space above and below the button */
        }
        .button {
            background-color: #5C2D91;
            color: #ffffff;
            padding: 18px 36px; /* Larger button with more padding */
            text-decoration: none;
            font-weight: bold;
            border-radius: 5px;
            display: inline-block;
            font-size: 16px;
        }
        .button:hover {
            background-color: #4b4e91; /* Darker purple on hover */
        }
        .email-footer {
            background-color: #f4f4f4;
            text-align: left; /* Justificar el texto a la izquierda */
            padding: 15px; /* Reducción del padding para menos espacio */
            font-size: 12px;
            color: #777777;
            border-top: 1px solid #dddddd;
            margin-top: 20px; /* Deja espacio entre el contenido principal y el footer */
            width: 100%; /* Asegura que el footer ocupe todo el ancho */
        }
        .email-footer a {
            color: #5C2D91;
            text-decoration: none;
        }
        .email-footer a:hover {
            text-decoration: underline;
        }
        .email-footer p {
            margin: 0; /* Eliminar margen para que los párrafos estén pegados */
            padding: 0; /* Eliminar relleno para que no haya espacio */
        }
	</style>
</head>
<body>
<div class="email-container rs-border-c2"><!-- Header with Logo -->
<div class="email-header"><img alt="Company Logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Proximus_logo_2014.svg/1280px-Proximus_logo_2014.svg.png" /></div>
<!-- Message Body -->

<div class="email-body"><!-- You can insert your message here --></div>
<!-- Button -->

<div class="button-container"><a class="button" href="http://yourlink.com">Click Here</a></div>
</div>
<!-- Footer -->

<div class="email-footer">
<p>You received this email as part of a <strong>Proximus Teams Notification</strong>.</p>

<p>All rights reserved. <a href="#">&copy; 2025 Proximus</a> | <a href="#">Legal warnings</a> | <a href="#">Privacy</a></p>

<p>Proximus PLC under Belgian Public Law, Bd. du Roi Albert II 27, B-1030 Brussels, Belgium,</p>

<p>VAT BE 0202.239.951, Brussels Register of Legal Entities, Giro BE82 2100 0008 8968</p>
</div>
</body>
</html>
    """
    return landing_page