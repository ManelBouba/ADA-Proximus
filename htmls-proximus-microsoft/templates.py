# Microsoft Team Template:
html_microsoft_template = '''
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Teams Style Email</title>
	<style type="text/css">body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f3f2f1;
            margin: 0;
            padding: 0;
        }
        .email-container {
            width: 100%;
            max-width: 650px; 
            margin: 40px auto;
            background-color: #ffffff;
            border: 1px solid #e1dfdd;
            border-radius: 12px; 
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15); 
            overflow: hidden;
        }
        .email-header {
            text-align: left;
            padding: 20px 30px;
        }
        .email-header img {
            max-width: 280px; 
            height: auto;
            display: block;
        }
        .email-body {
            padding: 30px; 
            color: #323130;
            font-size: 16px; 
            line-height: 1.8;
        }
        .email-body h1 {
            font-size: 22px;
            color: #323130;
            margin-bottom: 20px;
        }
        .button-container {
            text-align: center;
            margin: 30px 0; 
        }
        .button {
            background-color: #4E5FBF; 
            color: #ffffff;
            padding: 14px 28px; 
            text-decoration: none;
            font-weight: bold;
            border-radius: 8px; 
            display: inline-block;
            font-size: 16px;
        }
        .button:hover {
            background-color: #4b4e91; 
        }
        .email-footer {
            background-color: #f3f2f1;
            text-align: center;
            padding: 20px; 
            color: #605e5c;
            font-size: 14px;
            border-top: 1px solid #e1dfdd;
        }
        .email-footer a {
            color: #6264a7;
            text-decoration: none;
        }
        .email-footer a:hover {
            text-decoration: underline;
        }
        .email-footer img {
            margin-top: 10px; 
            max-width: 100px; 
            height: auto;
        }
	</style>
</head>
<body>
<div class="email-container"><!-- Header with Logo -->
<div class="email-header"><img alt="Microsoft Teams Logo" 
src="https://www.businessmobiles.com/wp-content/uploads/2021/11/Microsoft-Teams-Emblem-e1637851302489.png" /></div>
<!-- Message Body -->

<div class="email-body">
<h1>{subject}</h1>

<p>{body}</p>
</div>
<!-- Button -->

<div class="button-container"><a class="button" href="{link_url}">{link_text}</a></div>
</div>
<!-- Footer -->

<div class="email-footer">
<p>You received this email as part of a Microsoft Teams Notification.</p>

<p>Copyright 2025, Microsoft Corporation.</p>

<p><a href="https://privacy.microsoft.com/en-us/privacystatement">Privacy statement</a></p>

<p>Microsoft Corporation, One Microsoft Way, Redmond WA 98052 USA</p>
<img alt="Microsoft Logo" 
src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Microsoft_logo_%282012%29.svg/1280px-Microsoft_logo_%282012%29.svg.png" /></div>
</body>
</html>
'''
# Proximus Team Template:
html_proximus_template = '''
Proximus Template:
<!DOCTYPE html>
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
'''