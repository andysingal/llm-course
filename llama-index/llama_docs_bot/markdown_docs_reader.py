import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, cast

from llama_index import SimpleDirectoryReader
from llama_index.readers.base import BaseReader
from llama_index.schema import Document, NodeRelationship, RelatedNodeInfo


class MarkdownDocsReader(BaseReader):
    """MarkdownDocsReader

    Extract text from markdown files into Document objects.
    """

    def __init__(
        self,
        *args: Any,
        remove_hyperlinks: bool = True,
        remove_images: bool = True,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)
        self._remove_hyperlinks = remove_hyperlinks
        self._remove_images = remove_images

    def markdown_to_docs(self, markdown_text: str, filename: str) -> List[Document]:
        """Convert a markdown file to a dictionary.

        The keys are the headers and the values are the text under each header.

        """
        markdown_docs: List[Document] = []
        lines = markdown_text.split("\n")

        header_stack = []
        current_header_level = 0
        current_text = ""
        current_code_block = ""

        for line in lines:
            header_match = re.match(r"^#+\s", line)
            code_match = re.match(r"^```", line)
            if header_match:
                # save the current text
                if current_text.strip() != "":
                    link_matches = re.findall(r"\[.*\]\(.*\)", current_text)
                    links = []
                    for link_match in link_matches:
                        link_text = link_match.split("](")[0].replace("[", "")
                        link_url = link_match.split("](")[1].replace(")", "")
                        links.append(f"(link_text: {link_text}, link_url: f{link_url})")
                    markdown_docs.append(
                        Document(
                            text=current_text.strip(),
                            metadata={
                                "File Name": filename, 
                                "Content Type": "text",
                                "Header Path": "/".join(header_stack),
                                "Links": ", ".join(links),
                            },
                        )
                    )
                    current_text = ""

                # update the header stack
                header_level = line.count("#")
                header_text = line.replace("#", "").strip()
                if header_level > current_header_level:
                    header_stack.append(header_text)
                    current_header_level = header_level
                else:
                    header_stack.pop()
                    header_stack.append(header_text)
            elif code_match or current_code_block:
                if code_match and current_code_block:
                    current_code_block += line + "\n"
                    if len(markdown_docs) > 0 and markdown_docs[-1].metadata['Header Path'] == '/'.join(header_stack):
                        markdown_docs.append(
                            Document(
                                text=current_code_block.strip(),
                                metadata={
                                    "File Name": filename, 
                                    "Content Type": "code",
                                    "Header Path": "/".join(header_stack),
                                },
                                relationships={
                                    NodeRelationship.PARENT: RelatedNodeInfo(
                                        node_id=markdown_docs[-1].id_,
                                    )
                                }
                            )
                        )
                    else:
                        markdown_docs.append(
                            Document(
                                text=current_code_block,
                                metadata={
                                    "File Name": filename, 
                                    "Content Type": "code",
                                    "Header Path": "/".join(header_stack),
                                },
                            )
                        )
                    current_code_block = ""
                elif code_match and current_text.strip() != "":
                    link_matches = re.findall(r"\[.*\]\(.*\)", current_text)
                    links = []
                    for link_match in link_matches:
                        link_text = link_match.split("](")[0].replace("[", "")
                        link_url = link_match.split("](")[1].replace(")", "")
                        links.append(f"(link_text: {link_text}, link_url: f{link_url})")
                    markdown_docs.append(
                        Document(
                            text=current_text.strip(),
                            metadata={
                                "File Name": filename, 
                                "Content Type": "text",
                                "Header Path": "/".join(header_stack),
                                "Links": ", ".join(links),
                            },
                        )
                    )
                    current_text = ""
                else:
                    current_code_block += line + "\n"
            else:
                current_text += line + "\n"
        
        # catch remaining text
        if current_text.strip() != "":
            markdown_docs.append(
                Document(
                    text=current_text.strip(),
                    metadata={
                        "File Name": filename, 
                        "Content Type": "text",
                        "Header Path": "/".join(header_stack),
                    },
                )
            )
            current_text = ""

        return markdown_docs

    def remove_images(self, content: str) -> str:
        """Get a dictionary of a markdown file from its path."""
        pattern = r"!{1}\[\[(.*)\]\]"
        content = re.sub(pattern, "", content)
        return content

    def remove_hyperlinks(self, content: str) -> str:
        """Get a dictionary of a markdown file from its path."""
        pattern = r"\[(.*?)\]\((.*?)\)"
        content = re.sub(pattern, r"\1", content)
        return content

    def parse_tups(self, filepath: Path,) -> List[Document]:
        """Parse file into tuples."""

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        if self._remove_hyperlinks:
            content = self.remove_hyperlinks(content)
        if self._remove_images:
            content = self.remove_images(content)
        markdown_docs = self.markdown_to_docs(content, str(filepath))
        return markdown_docs

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file into string."""
        documents = self.parse_tups(file)

        # add additional extra info to metadata
        for doc in documents:
            doc.metadata.update(extra_info or {})

        return documents
