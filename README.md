# Micromix user guide

## Contents
- [Micromix](#micromix)
- [Installing and running](installing_running.md)
    - [Using pre-built AWS container](installing_running.md#1-using-pre-built-aws-container)
    - [Local install](installing_running.md#2-running-locally-or-on-a-server)
        - [Website](installing_running.md#website)
        - [Heatmap](installing_running.md#heatmap)
- [Using Micromix](using_micromix.md)
- [Modifying Micromix](modifying_micromix.md)
    - [Preparing a new bacteria](modifying_micromix.md#preparing-a-new-bacteria)
    - [How to add a new organism](modifying_micromix.md#how-to-add-a-new-organism)
    - [How to add new expression data](modifying_micromix.md#how-to-add-new-expression-data)
    - [Modifying or adding gene or pathway annotations](modifying_micromix.md#modifying-or-adding-gene-or-pathway-annotations)
    - [Adding new visualisation plugins](modifying_micromix.md#adding-new-visualisation-plugins)


<br><br>


# Micromix

## Background
Micromix was designed as a visualisation platform to easily view next generation sequencing data, such as counts from RNA-seq. Its main focus is for use with prokaryotic data, such as bacteria, which comes pre-bundled. Different bacteria can be included where the associated data can be filtered and/or transformed, then passed through a visualisation tool to examine biological patterns further, such as a heatmap.


## Infrastructure
The site contains a backend (Flask) and frontend (Vue.js) that communicate with each other, saving data from each session using MongoDB. Plugins within the site are typically setup on separate servers with data being passed and a visualisation returned and displayed within the site.
Since each user session is stored with a unique ID, session information can be re-loaded by passing the unique ID into the URL. For example: http://micromix.com?config=63ec9a4be1ea830ca6249f46. These types of links can also be shared to collaborators so they can examine specific data patterns from data within the site, or unique user data they have manually uploaded.

<br>
<br>

<img width="80%" src="images/micromix_inf.png" />

