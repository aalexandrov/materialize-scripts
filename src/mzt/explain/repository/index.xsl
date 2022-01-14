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
                    <div class="row mt-3">
                        <div class="col">
                            <h1 class="text-center">Explain Plan Repository</h1>
                        </div>
                    </div>
                    <div class="row" id="display-mode">
                        <div class="col">
                            <div class="custom-control custom-switch">
                                <input class="custom-control-input" type="checkbox" value="" id="raw-plan" />
                                <label class="custom-control-label" for="raw-plan">raw plan</label>
                            </div>
                            <div class="custom-control custom-switch">
                                <input class="custom-control-input" type="checkbox" value="" id="typed-raw-plan" />
                                <label class="custom-control-label" for="typed-raw-plan">raw plan (typed)</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="custom-control custom-switch">
                                <input class="custom-control-input" type="checkbox" value="" id="decorrelated-plan" />
                                <label class="custom-control-label" for="decorrelated-plan">decorrelated plan</label>
                            </div>
                            <div class="custom-control custom-switch">
                                <input class="custom-control-input" type="checkbox" value="" id="typed-decorrelated-plan" />
                                <label class="custom-control-label" for="typed-decorrelated-plan">decorrelated plan (typed)</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="custom-control custom-switch">
                                <input class="custom-control-input" type="checkbox" value="" id="optimized-plan" />
                                <label class="custom-control-label" for="optimized-plan">optimized plan</label>
                            </div>
                            <div class="custom-control custom-switch">
                                <input class="custom-control-input" type="checkbox" value="" id="typed-optimized-plan" />
                                <label class="custom-control-label" for="typed-optimized-plan">optimized plan (typed)</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="custom-control custom-switch">
                                <input class="custom-control-input" type="checkbox" value="" id="query-graph" />
                                <label class="custom-control-label" for="query-graph">query graph</label>
                            </div>
                            <div class="custom-control custom-switch">
                                <input class="custom-control-input" type="checkbox" value="" id="typed-query-graph" />
                                <label class="custom-control-label" for="typed-query-graph">query graph (typed)</label>
                            </div>
                        </div>
                    </div>
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
                            <div class="col mode-raw-plan d-none">
                                <h4 class="text-center">raw plan</h4>
                                <img src="{id}/raw-plan.svg" alt="raw" class="img-fluid" />
                            </div>
                            <div class="col mode-typed-raw-plan d-none">
                                <h4 class="text-center">raw plan (typed)</h4>
                                <img src="{id}/typed-raw-plan.svg" alt="raw" class="img-fluid" />
                            </div>
                            <div class="col mode-decorrelated-plan d-none">
                                <h4 class="text-center">decorrelated plan</h4>
                                <img src="{id}/decorrelated-plan.svg" alt="decorrelated" class="img-fluid" />
                            </div>
                            <div class="col mode-typed-decorrelated-plan d-none">
                                <h4 class="text-center">decorrelated plan (typed)</h4>
                                <img src="{id}/typed-decorrelated-plan.svg" alt="decorrelated" class="img-fluid" />
                            </div>
                            <div class="col mode-optimized-plan d-none">
                                <h4 class="text-center">optimized plan</h4>
                                <img src="{id}/optimized-plan.svg" alt="optimized" class="img-fluid" />
                            </div>
                            <div class="col mode-typed-optimized-plan d-none">
                                <h4 class="text-center">optimized plan (typed)</h4>
                                <img src="{id}/typed-optimized-plan.svg" alt="optimized" class="img-fluid" />
                            </div>
                            <div class="col mode-optimized-plan d-none">
                                <h4 class="text-center">query graph</h4>
                                <img src="{id}/query-graph.svg" alt="optimized" class="img-fluid" />
                            </div>
                            <div class="col mode-typed-optimized-plan d-none">
                                <h4 class="text-center">query graph (typed)</h4>
                                <img src="{id}/typed-query-graph.svg" alt="optimized" class="img-fluid" />
                            </div>
                        </div>
                    </xsl:for-each>
                </div>
                
                <!-- Optional JavaScript -->
                <!-- jQuery first, then Popper.js, then Bootstrap JS -->
                <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
                <script src="index.js" type="text/javascript"></script>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>