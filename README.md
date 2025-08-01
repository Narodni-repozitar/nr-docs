# Document part of the Czech National Repository

## Overview

Document part of the Czech National Repository (NR) is a digital repository system designed to manage and preserve digital content. It provides a platform for storing, sharing, and accessing
digital documents, ensuring their long-term availability and integrity.

## Installation and Setup

To install and set up this repository, follow these steps:

1. Create a `scripts/release-<version>.sh` file inside the `scripts` directory.
2. Build the docker image with the repository. 
   - create a deployment branch called `deployment/<version>`
   - go to https://github.com/oarepo/oarepo-deployment and run an action there to
     build the image
3. Ask devops to deploy the image to the production environment via the support channel.
   Pass them the following information:
    - the name of the repository (e.g., `nr-docs`)
    - version of the repository (e.g., `1.0.0`)
4. Devops will deploy the repository on a staging environment.
    - The repository will be available at https://docs.staging.narodni-repozitar.cz
5. The devops will run the `scripts/release-<version>.sh`. The initial deployment version
   will create the following:
   - users
   - roles
   - communities
   - import initial data
   Subsequent script might, for example, convert the data
6. To register repository owner(s):  (note 1)
   - the new owner must log in at least once before contacting devops
   - contact technical support via the support channel, passing the email of the new owner
     as it is in the user profile inside the repository.
   - technical support will run
      - `invenio roles add <email> request_manager`
      - `invenio roles add <email> communities_owner`
      - `invenio roles add <email> administration`
   - This command will:
      - add the person as an owner of all communities inside the repository
      - grants the person administration access to the repository, enabling
        the /administration interface
7. To remove a repository owner:    (note 1)
   - contact technical support to remove an owner, passing the email of the owner
     as it is in the user profile inside the repository.
   - technical support will run
      - `invenio roles remove <email> request_manager`
      - `invenio roles remove <email> communities_owner`
      - `invenio roles remove <email> administration`
8. Repository owner needs to log in and set up:
    - workflows for each created community if they are different from the default
      (for example, generic community). This is done on the community settings page.
    - set DOI mapping for each community that should provide DOIs (in administration
      pages - click on the "Administration" item in your profile menu).


Notes:

(1) Might be simplified in the future by having a group of owners inside PERUN
    and having specialized mechanism for synchronization of this group with the
    NTK repository.