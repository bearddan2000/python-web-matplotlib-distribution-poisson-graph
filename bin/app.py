from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from scipy.stats import poisson
from statistics import mean
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(
    __name__,
    instance_relative_config=False,
    template_folder="templates"
)

def create_graph():
    filename = 'demo'

    # random but consistant data
    lst = [2,9,4,6,4]
    plt.clf()
    fig, ax = plt.subplots(1, 1)
    mu = mean(lst)
    x = np.arange(poisson.ppf(0.01, mu),
              poisson.ppf(0.99, mu))
    ax.plot(x, poisson.pmf(x, mu), 'bo', ms=8, label='poisson pmf')
    ax.vlines(x, 0, poisson.pmf(x, mu), colors='y', lw=5, alpha=0.5)
    rv = poisson(mu)
    ax.vlines(x, 0, rv.pmf(x), colors='g', linestyles='-', lw=1, label='frozen pmf')
    ax.legend(loc='best', frameon=False)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    plt.ylabel('Probability %')
    plt.savefig(f'static/img/{filename}.png')

@app.route('/', methods=['GET'])
def getIndex():
    create_graph()
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5000, debug = True)