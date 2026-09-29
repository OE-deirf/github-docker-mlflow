# github-docker-mlflow
Simple Machine Learning demo using docker in github + MLFlow

# DVC, GIT  init
- git init
- dvc init            # create .dvc/ dir
- git commit -m "DVC init"

# DVC config
- dvc config core.autostage true        # after every dvc auto git add as well
- dvc config cache.type reflink,hardlink,symlink,copy   # cache -> workspace link type
- dvc config --list                      # actual config

# DVC remote
- dvc remote add -d storage s3://bucket/projekt     # -d = default remote
- dvc remote add backup /mnt/nas/dvc                # local / remote dir
- dvc remote add ssh_r ssh://user@host/path

# avoid secret to git:
- dvc remote modify --local storage access_key_id XXX
- dvc remote modify --local storage secret_access_key YYY

- dvc push        # cache -> remote
- dvc fetch       # remote-> cache
- dvc pull        # fetch + checkout

# DVC commit
- dvc add data/raw                    # -> data/raw.dvc + data/.gitignore
- git add data/raw.dvc data/.gitignore
- git commit -m "Data v1"
- dvc push

# DVC after modified data:
- dvc status
- dvc commit data/raw.dvc  # or just dvc add data/raw
- git commit -am "Data v2"
- dvc push

# checkout
- git pull
- git checkout v1.0
- dvc pull
- dvc checkout

# checkout only with old data version
- git checkout v1.0 -- data/raw.dvc
- dvc checkout data/raw.dvc

# dvg dag
- dvc repro          # rerun the changed stage
- git add dvc.yaml dvc.lock
- git commit -m "Pipeline"
- dvc push
- dvc dag            # print DAG
  - dvc dag --outs   # just files
  - dvc dag train    # just train and its anchients
  - dvc dag --dot | dot -Tpng -o dag.png    # Graphviz
  - dvc dag --mermaid / --md                # Mermaid diagram

# full example
# local
- vim params.yaml
- dvc repro
- dvc metrics diff
- git commit -am "lr=0.01"
- dvc push

# other local
- git pull
- dvc pull

# dvc system status
- dvc doctor
