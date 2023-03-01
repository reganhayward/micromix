# Micromix user guide

## Contents
- [Micromix](README.md#micromix-user-guide)
- [Installing and running](installing_running.md#micromix-user-guide)
    - [Using pre-built AWS container](installing_running.md#1-using-pre-built-aws-container)
    - [Local install](installing_running.md#2-running-locally-or-on-a-server)
        - [Website](installing_running.md#website)
        - [Heatmap](installing_running.md#heatmap)
- [Using Micromix](using_micromix.md#micromix-user-guide)
    - [Selecting organism](using_micromix.md#selecting-organism)
    - [Filtering data](using_micromix.md#filtering-data)
    - [Visualising data](using_micromix.md#visualising-data)  
- [Modifying Micromix](modifying_micromix.md#micromix-user-guide)
    - [Preparing a new bacteria](modifying_micromix.md#preparing-a-new-bacteria)
    - [How to add a new organism](modifying_micromix.md#how-to-add-a-new-organism)
    - [How to add new expression data](modifying_micromix.md#how-to-add-new-expression-data)
    - [Modifying or adding gene or pathway annotations](modifying_micromix.md#modifying-or-adding-gene-or-pathway-annotations)
    - [Adding new visualisation plugins](modifying_micromix.md#adding-new-visualisation-plugins)


<br><br>

# Modifying Micromix

Depending on the way you have configured or downloaded Micromix, when making changes, the frontend or backend (or both) may require restarting before the changes are visable.

If using the pre-configured image, you will have to restart the underlying service.

```bash
#Website
restart website-backend service
restart website-frontend service

#Heatmap
restart heatmap-backend service
restart heatmap-frontend service
```

If you have pre-compiled yourself, you only need to press `Control + C` to stop the service in the relevant terminal, then press the up arrow to find the previous command followed by `Enter`


## Preparing a new bacteria

Micromix can be used with any desired bacteria. Once a bacteria has been chosen, you will need to download and prepare some common files.
Here is a brief summary:

**Step 1:** download files

**Step 2:** Create transcriptome

**Step 3:** Create eggnog annotations

**Step 4:** Run script to generate .json files for micromix


In this example, we will use `Salmonella typhimurium SL1344`

**Step 1:**

Download the genome (.fasta or .fa) and genome annotation (.gff or .gtf).

For this example, you can use the following:

```bash
#GFF
curl https://ftp.ensemblgenomes.ebi.ac.uk/pub/bacteria/release-56/gff3/bacteria_79_collection/salmonella_enterica_subsp_enterica_serovar_typhimurium_str_sl1344_gca_000210855/Salmonella_enterica_subsp_enterica_serovar_typhimurium_str_sl1344_gca_000210855.ASM21085v2.56.chromosome.Chromosome.gff3.gz -o salmonella_sl1344.gff3.gz

#Fasta
curl https://ftp.ensemblgenomes.ebi.ac.uk/pub/bacteria/release-56/fasta/bacteria_79_collection/salmonella_enterica_subsp_enterica_serovar_typhimurium_str_sl1344_gca_000210855/dna/Salmonella_enterica_subsp_enterica_serovar_typhimurium_str_sl1344_gca_000210855.ASM21085v2.dna.chromosome.Chromosome.fa.gz -o salmonella_sl1344.fa.gz

#unzip
gunzip salmonella_sl1344.gff3.gz
gunzip salmonella_sl1344.fa.gz
```

**Step 2:**

Generate a bacterial transcriptome. This is required to upload to eggNOG-mapper [REF], which will provide annotations, including gene description, KEGG pathways, Gene Ontologies etc.

To get a summary of the features within your .gff file, you can run this command:

```bash
awk -F '\t' '{print $3}' salmonella_sl1344.gff3 | sort | uniq -c
```

This will display something similar to this:

```bash
awk -F '\t' '{print $3}' salmonella_sl1344.gff3 | sort | uniq -c
   4622 
    129 biological_region
   4466 CDS
      1 chromosome
   4636 exon
   4462 gene
   4462 mRNA
    113 ncRNA
    113 ncRNA_gene
     40 pseudogene
     40 pseudogenic_transcript
```

To generate the transcriptome, we need to know what features we would like to use. For example, we may only want to look at CDS regions, or we may want to look at a wider range of features as shown:

```bash
#The generate_transcriptome.py script is located here:
/folder/generate_transcriptome.py

#T view the help menu
./generate_transcriptome.py -h

#To run, select the feature (CDS etc), and also the gene ID type. If available, we recommend using a tag that exists for each loci such as a locus tag (sl1344_0001), so un-named and hypothetical genes will be included. You will need to open the .gff file to identify what fields are available (alternatives are gene_id, ID, Name etc).
generate_transcriptome.py \
-fasta salmonella_sl1344.fa \
-gff salmonella_sl1344.gff3 \
-f ["CDS", "ncRNA", "pseudogene"] -a gene_id \
-o salmonella_sl1344.fa
```

> Note: Bacterial genome annotations (.gff/.gtf) can be challenging to work with due to non-uniformity, duplicate gene names and many other issues. You may receive an error message saying that some genes are duplicated, and thus a transcriptome couldn't be created. If this happens, open the .gff file and manually change the locus_tags. For example, if there are multiple SL1344_0010, change to SL1344_0010a and SL1344_0010b, then re-run.

**Step 3:**

You can now upload your transcriptome to eggNOG by browsing to `http://eggnog-mapper.embl.de/`. Select **CDS** as shown, then upload your transcriptome **upload sequences**.
Enter your **email address** and **submit** the job. You will receive an email that you need to click on, which will take you back to their site where you can start your job **Start job**.

**<< image to be inserted >>**

After a short time, you will receive another email providing a download link. 
[download xxx files], this is the file that is used in the next step.


**Step 4:**

The last step is extracting out the required information from the eggNOG output and saving to a compatible format for Micromix (.json files)

To do this, you will need to run the following

```bash
#The script is located here 
/folder/script.R

#R will need to be installed on your machine for this to execute successfully

#The resulting output files will be saved in the current directory
./scripr.R eggnog.xxx

#After running, you should have the following two files:
genes.json
pathways.json
```

## How to add a new organism

The corresponding file should then be added as an entry to datasets.json
```
b-theta/website/frontend/src/assets/json/organisms.json

```
Here we have added **Bacteria B** with the corresponding tags:

`"name":` - The name of the bacteria (displayed on button)

`"description":` - The description (displayed on button)

`"path":` - This automatically points to `b-theta/website/frontend/src/assets/organisms/`. You should copy the default folder and rename to your new bacterial name. Within this folder is an icon you can update which is displayed on the button. You can also adit the file `filters.json` to add/modify/create custom filters (discussed below in more detail in the section **[xxx]**).

`"id":` - this is a string and hex numbers that should be unique for each bacteria

`"datasets":` - should link to an entry in this file: `b-theta/website/frontend/src/assets/json/datasets.json`. 


```json
{
  "items": {

    "Bacteria A": {
      "name": "Bacteria A",
      "description": "Manually select datasets.",
      "path": "/bacteriaA",
      "id": "bacteria-a-e2ad6b25-40cb-4594-8685-f4fcb3ceb0e7",
      "datasets": ["Bacteria A RNA-seq"]
    },
    "Bacteria B": {
      "name": "Bacteria B",
      "description": "Manually select datasets.",
      "path": "/BacteriaB",
      "id": "bacteria-a-e2ad6b25-40cb-4594-8685-f4fcb3ceb0e8",
      "datasets": ["Bacteria B RNA-seq"]
    }
  }
}
```
> After adding new organism, you will need to link it to the  expression data - see the next section


## How to add new expression data

###### not just expression data - other related data types include:::

Expression files should be saved here:

```
b-theta/website/backend/static/new_expression.tsv
```

The corresponding file should then be added as an entry to datasets.json
```
b-theta/website/frontend/src/assets/json/datasets.json

```

Each new entry requires all the fields presented here, such as `text`, `value` and `separator`. The new entry here is called **New dataset** and is linked to the file **new_data.tsv** that should have previously been saved.

Here is a brief description of the file contents:

`"Micromix RNA-seq":` - The is the bold value that cannot be selected in the dropdown menu when selecting a new dataset

`"text": "Dataset 1" ` and `"text": "New dataset" ` - these are the names that will appear in the dropdown box that when selected will load expression data

`"value": ` - this contains the filename with the expression data, the delimiter and decimal character. 

The `columns` field should contain all columns within the associated file - here, this would be `dataset1.tsv`. If the column names do not match, an error will occur.

If you would not like to immediately show all columns, you can decide which columns should initially be displayed with `pre_selected_columns`. They can be re-added by the user when selecting the data and selecting `choose additional columns...`.  

```json
{
  "Bacteria A RNA-seq": {
    "label": "Bacteria A RNA-seq",
    "options": [
      {
        "text": "Dataset 1",
        "value": {"filename": "dataset1.tsv", 
                  "seperator": "\t", 
                  "decimal_character": ".", 
                  "columns": [{"value": null, "text": "All columns"}, "Sequence name", "locus tag", "Name", "Start", "End", "Strand", "Condition 1 logFC", "Condition 2 logFC"]},
        "seperator": "\t"
      },
      {
        "text": "New dataset",
        "value": {"filename": "new_data.tsv", 
                  "seperator": "\t", 
                  "decimal_character": ".", 
                  "columns": [{"value": null, "text": "All columns"}, "Sequence name", "locus tag", "Name" "Start", "End", "Strand", "Condition 1 logFC"], 
                  "pre_selected_columns": ["locus tag", "Name", "Condition 1 logFC"]},
        "seperator": "\t"
      }

    ]
  }
}
```
> After adding new expression data, both the frontend and backend will require a restart


## Modifying or adding gene or pathway annotations

#where to look

using a script linking eggnog...
```bash
Rscript parse_eggnog_annotations.R eggnog_annotation.tsv
```


## Adding new visualisation plugins

Buttons can do many things,
Link to a different API - clustergrammer
Link to website - jbrowse
Link to a custom API - heatmap

Info stored in [  ] and should be assigned a unique HEX number, such as xxx. 
Each plugin is stored in [  ]. Open the corresponding files to examine how information is parsed.




8.	How to deploy on a server and config files – nginx and gunicorn



To update gene annotations and pathways

Frontend
Src/assets/organisms/bacteroides/pathways.json
Src/assets/organisms/bacteroides/filters.json
Src/components/search_query.vue

Backend
Static/gene_annotations.json
