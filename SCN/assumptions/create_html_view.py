from decouple import config
import os


class HTML_file:
    def __init__(self, group_name: str) -> None:
        self.group_name = group_name
        self.png_dir = os.path.join(config('root'), 'work/visual_graphs')

    def save_directory(self) -> str:
        return os.path.join(config('root'), 'results/assumptions')

    def html_markup(self) -> str:

        html_head_css = """
        <!DOCTYPE html>
        <html>
        <head>
            <style type="text/css" media="screen">
                body{background-color: azure; font-family: "Arial", Arial, Sans-serif;}
            </style>
        """
        
        html_body = f"""
                 <title>Assumption graphs for {self.group_name}</title>
        </head>
        <body>
          <h1>Distro plots for average clustering, average shortest path length, assortativity, modularity and efficieny</h1>
          <centre>
          <img src="{self.png_dir}/distro_plots_{self.group_name}.png">
        </centre>
          <h1>Network measure plots</h1>
            <center>
            <img src="{self.png_dir}/network_measures_plot_{self.group_name}.png">
        </center>
        </body>
        </html>
        """
        return html_head_css + html_body

    def save_to_file(self) -> None:
        directory = self.save_directory() + f'/{self.group_name}_assumptions.html'
        html = self.html_markup()
        with open(directory, 'w') as file:
            file.write(html)
