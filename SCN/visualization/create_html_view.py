from decouple import config
import os


class HTML_file:
    def __init__(self, group_name: str, measure: str) -> None:
        self.group_name = group_name
        self.measure = measure
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
          <img src="{self.png_dir}/distro_plots_for_{self.group_name}_for_{self.measure}.png">
        </centre>
          <h1>Network measure plots</h1>
            <center>
            <img src="{self.png_dir}/network_measures_plot_for_{self.group_name}_for_{self.measure}.png">
        </center>
        </body>
        </html>
        """
        return html_head_css + html_body

    def save_to_file(self) -> None:
        directory = self.save_directory() + f'/{self.group_name}_assumptions_for_{self.measure}.html'
        html = self.html_markup()
        with open(directory, 'w') as file:
            file.write(html)

class Group_differences_HTML_file:
    def __init__(self, groups: dict, measure: str) -> None:
        self.png_dir = os.path.join(config('root'), 'work/visual_graphs')
        self.groups = [key for key in groups]
        self.measure = measure

    
    def save_directory(self) -> str:
        return os.path.join(config('root'), 'results/group_differences')
    
    def img_src(self):
        img_src = f"""
        <h2> Cluster plot for {self.groups[0]} </h2>
        <img src="{self.png_dir}/cluster_plots_for_{self.groups[0]}_for_{self.measure}.png">
        <h2> Cluster plot for {self.groups[1]} </h2>
        <img src="{self.png_dir}/cluster_plots_for_{self.groups[1]}_for_{self.measure}.png">
        """

        if len(self.groups) == 3:
            img_src = img_src + f"""
            <h2> Cluster plot for {self.groups[2]} </h2>
            <img src="{self.png_dir}/cluster_plots_for_{self.groups[2]}_for_{self.measure}.png">
            """      
        
        return img_src

    def html_markup(self) -> str:
        img = self.img_src()
        html_head_css = """
        <!DOCTYPE html>
        <html>
        <head>
            <style type="text/css" media="screen">
                body{background-color: azure; font-family: "Arial", Arial, Sans-serif;}
            </style>
        """
        
        html_body = f"""
                 <title>Group difference graphs</title>
        </head>
        <body>
          <h1>Cluster plots</h1>
          <centre>
          {img}
        </centre>
        </body>
        </html>
        """
        return html_head_css + html_body

    def save_to_file(self) -> None:
        directory = self.save_directory() + f'/group_differences_for_{self.measure}.html'
        html = self.html_markup()
        with open(directory, 'w') as file:
            file.write(html)
        