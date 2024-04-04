def html():
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Report</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="title-container">
        (TITLE_REPORT)
    </div>
    <article>
        <div class="report">
            (CONTENT_DEMOGRAPHICS)
        </div>
    </article>
    <aside>
        <div class="numbers">
            <div class="lsitin">
                (LISTING_REPORT)
            </div>
            <div class="score">
                (SCORE_REPORT)
            </div>
        </div>
    </aside>
    <footer>
        <i>Cretaed by, <a href="https://camiworks.github.io/CamiWorks/">Camilo Sierra Lozano</a></i>
    </footer>
</body>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script src="script.js"></script>
</html>
"""


def html_title(address: str) -> str:
    return f"<h1>Report of {address}</h1>"


def css_tempalte() -> str:
    return """
    body{
    color: black;
    font-family: Arial, Helvetica, sans-serif;
}
.title-container{
    text-align: center;
}
.report, .numbers{
    display: flex;
    flex-wrap: wrap;
}
.numbers div{
    min-width: 45%;
    text-align: center;
    justify-content: space-around;
    padding: 10px;
}
.report div{
    min-width: 32%;
    text-align: center;
    justify-content: space-around;
    padding: 10px;
}
.numbers span{
    font-size: 30px;
    font-weight: 30;
}
footer{
    padding: 20px;
}

"""
