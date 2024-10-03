import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from pathlib import Path
from src import structure

system_role = """
You are an expert in structured data extraction. Your task is to convert unstructured text from CA/Browser Forum documents into a structured format that meets specific requirements. The structured output will be used in a GRC system to ensure compliance with the document. Your goal is to identify and clearly articulate each requirement from the text.

You will strictly adhere to these rules:

- You write requirements based on the text provided. If the text does not contain a requirement, you should not invent one and return an empty list.
- You write requirements, no recommendations or statements.
- You will use the appropiate context and must replace "this method" or "this section" with the actual method name or section number (provided in the title).
- **Comprehensive Coverage**: Identify all requirements in the text, ensuring that no requirement is overlooked. It is better to include more requirements than to miss any.
- **Granular Extraction**: Each requirement must be listed as a separate item. One paragraph may contain multiple requirements.
- **Detail-Oriented**: You should identify both explicit and implicit requirements. Include actions that make the requirements verifiable and auditable.
- **Clarity and Precision**: Write requirements that are unambiguous, clear, and self-contained. Avoid nesting requirements (e.g., "If X, then Y, and if Y, then Z").
- **Use of RFC 2119 Language**: Each requirement must include RFC 2119 keywords (e.g., MUST, MUST NOT, SHALL, SHOULD, MAY) to indicate the requirement level.
- **Who, What, Why**: Each requirement should address who is responsible, what action is required, and why (if applicable).
- **Conditional Requirements**: Requirements may be conditional (e.g., "If X, then Y"). Multiple options should be broken down into one overall requirement and multiple conditional sub-requirements.
- **Present Tense**: Write all requirements in the present tense.
- **Explicit References**: Avoid undefined references like "as specified in the document" or "using one of the specified methods." Explicitly name the section or method.
- **Subject Specificity**: Clearly state the subject of the requirement. Avoid generic terms like "the document." Instead, use specific references (e.g., "Certificate," "Subject," "CRL," "CP," "CPS," "Subscriber Agreement," "Terms and Conditions").
- **Brevity and Completeness**: Each requirement should be concise (under 400 characters) yet comprehensive and verifiable/auditable.
- **Abbreviations**: Use common PKI abbreviations where appropriate (e.g., CP, CPS, CRL, OCSP).

### Example:

Given the following text:

```
#### 3.2.2.3 Verification of Country

If the `subject:countryName` field is present, then the CA SHALL verify the country associated with the Subject using one of the following:

  a. the IP Address range assignment by country for either
     i. the web site's IP address, as indicated by the DNS record for the web site or
     ii. the Applicant's IP address;
  b. the ccTLD of the requested Domain Name;
  c. information provided by the Domain Name Registrar; or
  d. a method identified in [Section 3.2.2.1](#3221-identity).

The CA SHOULD implement a process to screen proxy servers in order to prevent reliance upon IP addresses assigned in countries other than where the Applicant is actually located.
```

You should produce the following structured requirements:

```
- If the subject:countryName field is present, the CA SHALL verify the country associated with the Subject.
- The CA MAY verify the country using the IP Address range assignment by country for the web site's IP address as indicated by the DNS record.
- The CA MAY verify the country using the IP Address range assignment by country for the Applicant's IP address.
- The CA MAY verify the country using the ccTLD of the requested Domain Name.
- The CA MAY verify the country using information provided by the Domain Name Registrar.
- The CA MAY verify the country using a method identified in Section 3.2.2.1.
- The CA SHOULD implement a process to screen proxy servers to prevent reliance on IP addresses assigned in countries other than where the Applicant is actually located.
```

"""

skip_sections = ['1.2.1','1.2.2', '1.6']

class Requirements(BaseModel):
    requirements: list[str]

def get_requirements(content):
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": content}
        ],
        response_format=Requirements
    )

    msg = response.choices[0].message

    # If the model refuses to respond, you will get a refusal message
    if (msg.refusal):
        print(msg.refusal)
        return []
    else:
        return msg.parsed


def main():
    parser = argparse.ArgumentParser(
        description='Extract requirements in each section')
    parser.add_argument('-in', '--input', default='../structured/', type=str,
                        help='input directory')
    parser.add_argument('-type', '--type', default='', type=str,
                        help='filter document type, e.g., BR, TLS, EVG, CS, SMIME, etc.')
    args = parser.parse_args()

    p = Path(args.input)
    files = sorted(p.rglob("*.md"))

    for file in files:
        # Filter files by type
        type = structure.get_type(file)
        if args.type:
            if type != args.type:
                continue

        # Skip requirements files
        if f"100_{type}" in file.name:
            continue

        # Name of the requirements file
        requirements_filename = file.name.replace("000_", "100_")

        # Remove an existing requirements file if it exists
        if file.with_name(requirements_filename).exists():
            os.remove(file.with_name(requirements_filename))

        # Get section number
        section = structure.get_section(file)

        # Skip sections that are not requirements
        if section == "":
            continue

        for sec in skip_sections:
            if section.startswith(sec):
                continue

        print(f"Extracting requirements from {type} section {section} in {file.name}")
        
        try:
            with file.open(encoding="utf8") as file_content:
                content = file_content.read()

                # Skip if there is only a title
                if content.strip().count('\n') <= 2:
                    continue

                req = get_requirements(content)
                if len(req.requirements) > 0:
                    print(f"Requirements found in {type} section {section} ({file.name})")

                    # Write the requirements to a file
                    with open(file.with_name(requirements_filename), 'w', encoding='utf-8') as requirements_file:
                        for id, content in enumerate(req.requirements):
                            req = f"    [{str(id).zfill(3)}] {content}\n"
                            requirements_file.write(req)
                            print(req)

                        requirements_file.close()
                else:
                    print(f"No requirements found in {type} section {section} ({file.name})")

        except Exception as e:
            print(f"Error while processing file {file}: {e}")


if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        client = OpenAI(api_key=api_key)
        main()
    else:
        print("OpenAI API key not provided. Please set OPENAI_API_KEY in the environment or .env file.")
