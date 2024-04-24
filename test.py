<!DOCTYPE html>
<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body>

    <h2>Check Status</h2>

    <div class="modal">
        
    </div>

    <div class="modal">

        <form action="/check" method="post">

            <div class="container">
                <b>Select the Web Application</b>
                <input type="radio" id="main" name="webapp_selector" value="http://vulnerablesite.htb">
                <label for="main">vulnerablesite.htb</label><br>
                <input type="radio" id="internal" name="webapp_selector" value="http://internal.vulnerablesite.htb">
                <label for="internal">internal.vulnerablesite.htb</label><br>
                <input type="radio" id="api" name="webapp_selector" value="http://api.vulnerablesite.htb">
                <label for="api">api.vulnerablesite.htb</label>

                <button type="submit">Check</button>
            </div>
        </form>
    </div>

</body>

</html>