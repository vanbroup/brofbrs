#!/bin/bash

export PYTHONUTF8=1
set -e

mkdir -p ../docs ../structured ../output ../public

echo "::group::Remove existing structured documents"
rm -rf ../structured/*
echo "::endgroup::"

echo "::group::Update source documents"
curl -s -o ../docs/BR.md https://raw.githubusercontent.com/cabforum/servercert/main/docs/BR.md
curl -s -o ../docs/EVG.md https://raw.githubusercontent.com/cabforum/servercert/main/docs/EVG.md
curl -s -o ../docs/CS.md https://raw.githubusercontent.com/cabforum/code-signing/main/docs/CSBR.md
curl -s -o ../docs/SMIME.md https://raw.githubusercontent.com/cabforum/smime/main/SBR.md
echo "::endgroup::"

echo "::group::Tranforming documents"
python transform.py ../docs/BR.md
python transform.py ../docs/EVG.md
python transform.py ../docs/CS.md
python transform.py ../docs/SMIME.md
echo "::endgroup::"

echo "::group::Remove duplicates"
python duplicates.py | tee ../duplicates.md
echo "::endgroup::"

# echo "::group::Add examples"
# cp -rv testlayers/* ../structured/
# echo "::endgroup::"

echo "::group::Build documents"
python build.py BR
python build.py EVG
python build.py CS
python build.py SMIME
echo "::endgroup::"

echo "::group::Change Baseline Requirements files to TLS that should end up in the other documents"
python totls.py
echo "::endgroup::"

echo "::group::Using BR main document as a template for TLS"
cp -v ../structured/000_BR.md ../structured/000_TLS.md
sed -i 's/Certificates/TLS Certificates/g' ../structured/000_TLS.md
echo "::endgroup::"

echo "::group::Remove output"
rm -fv ../output/*
echo "::endgroup::"

echo "::group::Building documents again"
python build.py BR
python build.py EVG
python build.py CS
python build.py SMIME
python build.py TLS
echo "::endgroup::"

echo "::group::Extract requirements"
python extract_req.py
echo "::endgroup::"

echo "::group::Building documents with extracted requirements"
python build.py BR
python build.py EVG
python build.py CS
python build.py SMIME
python build.py TLS
echo "::endgroup::"

echo "::group::Create HTML pages"
mkdir -p ../public
python tohtml.py -out ../public/
echo "::endgroup::"

echo "Done"