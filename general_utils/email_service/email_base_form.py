
def base_email_form(body: str) -> str:
    """
    The function returns the base code to the email without the body
    """
    return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <title>Title</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
    
                html {{
                    margin: 20px;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }}
    
                .main {{
                    background-color: #f6f6f6;
                    align-content: center;
                    height: 100%;
                }}
    
                .img-job {{
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                    width: 80px;
                    height: 80px;
                }}
    
                .logo-con {{
                    width: 100%;
                    padding: 20px;
                    margin: 0 auto;
                }}
    
                .text-con {{
                    background-color: white;
                    height: 100%;
                    width: 400px;
                    margin: 0 auto;
                    padding: 10px;
                    border-radius: 3%;
                }}
    
                .btn-con {{
                    
                    
                    margin: auto;
                    width: 120px;
                    height: 60px;
                    

                }}
    
                .btn {{
                    padding: 16px 32px;
                    text-align: center;
                    text-decoration: none;
                    display: block;
                    font-size: 16px;
                    transition-duration: 0.4s;
                    cursor: pointer;
                    background-color: #008CBA;
                    border: 2px solid #008CBA;
                }}
    
                .btn:hover{{
                    background-color: white;
                    border: 2px solid #008CBA;
                }}
    
                .btn:hover p{{
                    color: #008CBA;
                }}
    
                .color-button {{
                    color: white;
    
                }}
    
                h2, h3 {{
                    text-align: center;
                }}
    
                .title {{
                    padding-top: 30px;
                }}
                
                .title_content {{
                    margin-top: 15px;
                }}
    
                .content {{
                    margin-top: 20px;
                }}
    
                footer {{
                    background-color: #f6f6f6;
                    height: 100px;
                    width: 100%
                }}
                
                p {{
                    text-align: center;
                }}
    
            </style>
            </head>
            {body}
            </html>
            """

