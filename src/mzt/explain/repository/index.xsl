<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" doctype-system="about:legacy-compat"/>
    <xsl:template match="/">
        <html lang="en">
            <head>
                <!-- Required meta tags -->
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
                
                <!-- Bootstrap CSS -->
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"/>
                
                <title>Explain Plan Repository</title>
            </head>
            <body>
                <div class="container">
                    <div class="row" style="margin-top: 1.5rem">
                        <div class="col">
                            <h1 class="text-center">Explain Plan Repository</h1>
                        </div>
                    </div>
                    <!-- <div class="row"><h2>Queries</h2></div> -->
                    <xsl:for-each select="./queries/query">
                        <hr />
                        <div class="row" style="margin-bottom: .5rem">
                            <blockquote class="blockquote" style="display: block; width: 100%;">
                                <pre><code><xsl:value-of select="./sql"/></code></pre>
                            </blockquote>
                            <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#Q-{id}" aria-expanded="false" aria-controls="Q-{id}">
                                toggle plans
                            </button>
                        </div>
                        <div class="row collapse" id="Q-{id}">
                            <div class="col">
                                <h4 class="text-center">raw plan</h4>
                                <img src="{id}/raw.svg" alt="raw" class="img-fluid" />
                            </div>
                            <div class="col">
                                <h4 class="text-center">decorrelated plan</h4>
                                <img src="{id}/decorrelated.svg" alt="decorrelated" class="img-fluid" />
                            </div>
                            <div class="col">
                                <h4 class="text-center">optimized plan</h4>
                                <img src="{id}/optimized.svg" alt="optimized" class="img-fluid" />
                            </div>
                        </div>
                    </xsl:for-each>
                    
                    <!-- 
                         <h2>Views</h2>
                         <xsl:for-each select="./views/view">
                         <h3>
                         <xsl:value-of select="."/>
                         [<a href="{.}/graph-0000.dot.png">raw</a>]
                         [<a href="{.}/graph-0001.dot.png">raw</a>]
                         [<a href="{.}/graph-0002.dot.png">raw</a>]
                         </h3>
                         <code><xsl:value-of select="."/></code>
                         </xsl:for-each>
                    -->
                    
                    <!-- Optional JavaScript -->
                    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
                    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
                    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>