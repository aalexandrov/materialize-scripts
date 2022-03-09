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
                    <form>
                        <div class="row mt-3">
                            <div class="col">
                                <h2>Display Settings</h2>
                            </div>
                        </div>
                        <fieldset class="row mt-3" id="display-plan">
                            <legend class="col-12">Plans to show</legend>
                            <div class="col">
                                <div class="custom-control custom-switch">
                                    <input class="custom-control-input" type="checkbox" value="display-mode" id="raw-plan" />
                                    <label class="custom-control-label" for="raw-plan">raw plan</label>
                                </div>
                                <div class="custom-control custom-switch">
                                    <input class="custom-control-input" type="checkbox" value="display-mode" id="query-graph" />
                                    <label class="custom-control-label" for="query-graph">query graph</label>
                                </div>
                                <div class="custom-control custom-switch">
                                    <input class="custom-control-input" type="checkbox" value="display-mode" id="optimized-query-graph" />
                                    <label class="custom-control-label" for="optimized-query-graph">optimized query graph</label>
                                </div>
                                <div class="custom-control custom-switch">
                                    <input class="custom-control-input" type="checkbox" value="display-mode" id="decorrelated-plan" />
                                    <label class="custom-control-label" for="decorrelated-plan">decorrelated plan</label>
                                </div>
                                <div class="custom-control custom-switch">
                                    <input class="custom-control-input" type="checkbox" value="display-mode" id="optimized-plan" />
                                    <label class="custom-control-label" for="optimized-plan">optimized plan</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="custom-control custom-switch">
                                    <input class="custom-control-input" type="checkbox" value="display-mode" id="typed-raw-plan" />
                                    <label class="custom-control-label" for="typed-raw-plan">typed raw plan</label>
                                </div>
                                <div class="custom-control custom-switch">
                                    <input class="custom-control-input" type="checkbox" value="display-mode" id="typed-query-graph" />
                                    <label class="custom-control-label" for="typed-query-graph">typed query graph</label>
                                </div>
                                <div class="custom-control custom-switch">
                                    <input class="custom-control-input" type="checkbox" value="display-mode" id="typed-optimized-query-graph" />
                                    <label class="custom-control-label" for="typed-optimized-query-graph">typed optimized query graph</label>
                                </div>
                                <div class="custom-control custom-switch">
                                    <input class="custom-control-input" type="checkbox" value="display-mode" id="typed-decorrelated-plan" />
                                    <label class="custom-control-label" for="typed-decorrelated-plan">typed decorrelated plan</label>
                                </div>
                                <div class="custom-control custom-switch">
                                    <input class="custom-control-input" type="checkbox" value="display-mode" id="typed-optimized-plan" />
                                    <label class="custom-control-label" for="typed-optimized-plan">typed optimized plan</label>
                                </div>
                            </div>
                        </fieldset>
                        <fieldset class="row mt-3" id="output-format">
                            <legend class="col-12">Output type</legend>
                            <div class="col-3">
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="output-format" id="output-format-svg" value=".svg" checked="checked" />
                                    <label class="form-check-label" for="output-format-svg">SVG</label>
                                </div>
                            </div>
                            <div class="col-9">
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="output-format" id="output-format-png" value=".png" />
                                    <label class="form-check-label" for="output-format-png">PNG</label>
                                </div>
                            </div>
                        </fieldset>
                    </form>
                    <div class="row mt-3">
                        <div class="col">
                            <h2>Queries</h2>
                        </div>
                    </div>
                    <xsl:for-each select="./queries/query">
                        <hr />
                        <div class="row" style="margin-bottom: .5rem">
                            <div class="col-12">
                                <blockquote class="blockquote" style="display: block; width: 100%;">
                                    <pre><code><xsl:value-of select="./sql"/></code></pre>
                                </blockquote>
                                <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#Q-{id}" aria-expanded="false" aria-controls="Q-{id}">
                                    toggle plans
                                </button>
                                <button class="btn btn-primary clipboard" type="button" style="margin-left: 0.5em;" data-content="{id}">
                                    copy query hash
                                </button>
                            </div>
                        </div>
                        <div class="row collapse" id="Q-{id}">
                            <div class="col mode-raw-plan d-none">
                                <h4 class="text-center">raw plan</h4>
                                <img src="{id}/raw-plan.svg" alt="raw-plan" onerror="this.src='not_available.png'" class="plan img-fluid" />
                            </div>
                            <div class="col mode-typed-raw-plan d-none">
                                <h4 class="text-center">typed raw plan</h4>
                                <img src="{id}/typed-raw-plan.svg" alt="typed-raw-plan" onerror="this.src='not_available.png'" class="plan img-fluid" />
                            </div>
                            <div class="col mode-query-graph d-none">
                                <h4 class="text-center">query graph</h4>
                                <img src="{id}/query-graph.svg" alt="query-graph" onerror="this.src='not_available.png'" class="plan img-fluid" />
                            </div>
                            <div class="col mode-typed-query-graph d-none">
                                <h4 class="text-center">typed query graph</h4>
                                <img src="{id}/typed-query-graph.svg" alt="typed-query-graph" onerror="this.src='not_available.png'" class="plan img-fluid" />
                            </div>
                            <div class="col mode-optimized-query-graph d-none">
                                <h4 class="text-center">optimized query graph</h4>
                                <img src="{id}/optimized-query-graph.svg" alt="optimized-query-graph" onerror="this.src='not_available.png'" class="plan img-fluid" />
                            </div>
                            <div class="col mode-typed-optimized-query-graph d-none">
                                <h4 class="text-center">typed optimized query graph</h4>
                                <img src="{id}/typed-optimized-query-graph.svg" alt="typed-optimized-query-graph" onerror="this.src='not_available.png'" class="plan img-fluid" />
                            </div>
                            <div class="col mode-decorrelated-plan d-none">
                                <h4 class="text-center">decorrelated plan</h4>
                                <img src="{id}/decorrelated-plan.svg" alt="decorrelated-plan" onerror="this.src='not_available.png'" class="plan img-fluid" />
                            </div>
                            <div class="col mode-typed-decorrelated-plan d-none">
                                <h4 class="text-center">typed decorrelated plan</h4>
                                <img src="{id}/typed-decorrelated-plan.svg" alt="typed-decorrelated-plan" onerror="this.src='not_available.png'" class="plan img-fluid" />
                            </div>
                            <div class="col mode-optimized-plan d-none">
                                <h4 class="text-center">optimized plan</h4>
                                <img src="{id}/optimized-plan.svg" alt="optimized-plan" onerror="this.src='not_available.png'" class="plan img-fluid" />
                            </div>
                            <div class="col mode-typed-optimized-plan d-none">
                                <h4 class="text-center">typed optimized plan</h4>
                                <img src="{id}/typed-optimized-plan.svg" alt="typed-optimized-plan" onerror="this.src='not_available.png'" class="plan img-fluid" />
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