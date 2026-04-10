---
title: "Introduction - Supadata Docs"
source: "https://docs.supadata.ai/api-reference/introduction"
original_link: "https://docs.supadata.ai/api-reference/introduction"
saved: 2026-04-09
words: 306
tags: []
---

[Skip to main content](https://docs.supadata.ai/api-reference/introduction#content-area)

[Supadata Docs home page![light logo](https://mintcdn.com/dumplingsoftware/Xu3Hs8dlpcBvOdeq/logo/light.svg?fit=max&auto=format&n=Xu3Hs8dlpcBvOdeq&q=85&s=a03fbe1144d27c3b28e29a717926ff15)![dark logo](https://mintcdn.com/dumplingsoftware/Xu3Hs8dlpcBvOdeq/logo/dark.svg?fit=max&auto=format&n=Xu3Hs8dlpcBvOdeq&q=85&s=f02bbd528545439b3588b973f3fdec8d)](https://docs.supadata.ai/)

Search...

Ctrl K

Search...

Navigation

Using the API

Introduction

[Documentation](https://docs.supadata.ai/) [Integrations](https://docs.supadata.ai/integrations/overview) [API Reference](https://docs.supadata.ai/api-reference/introduction)

On this page

- [Features](https://docs.supadata.ai/api-reference/introduction#features)
- [Base URL](https://docs.supadata.ai/api-reference/introduction#base-url)
- [Authentication](https://docs.supadata.ai/api-reference/introduction#authentication)
- [Response codes](https://docs.supadata.ai/api-reference/introduction#response-codes)
- [Rate limit](https://docs.supadata.ai/api-reference/introduction#rate-limit)

## [​](https://docs.supadata.ai/api-reference/introduction\#features)  Features

[**Transcript** \\
\\
Get social media or file transcript.](https://docs.supadata.ai/api-reference/endpoint/transcript/transcript)

[**Metadata** \\
\\
Get social media post metadata.](https://docs.supadata.ai/api-reference/endpoint/metadata/metadata)

[**Extract** \\
\\
Extract structured data from videos using AI.](https://docs.supadata.ai/api-reference/endpoint/extract/extract)

[**Web** \\
\\
Extract content from any website in markdown format.](https://docs.supadata.ai/api-reference/endpoint/web/scrape)

## [​](https://docs.supadata.ai/api-reference/introduction\#base-url)  Base URL

All requests contain the following base URL:

```
https://api.supadata.ai/v1
```

## [​](https://docs.supadata.ai/api-reference/introduction\#authentication)  Authentication

For authentication, it’s required to include a `x-api-key` header.

```
x-api-key: {YOUR_API_KEY}
```

## [​](https://docs.supadata.ai/api-reference/introduction\#response-codes)  Response codes

Supadata employs conventional HTTP status codes to signify the outcome of your requests.Typically, 2xx HTTP status codes denote success, 4xx codes represent failures related to the user, and 5xx codes signal infrastructure problems.

| Status | Description |
| --- | --- |
| 200 | Request was successful. |
| 400 | Verify the correctness of the parameters. |
| 401 | The API key was not provided. |
| 402 | Payment required. |
| 404 | The requested resource could not be located. |
| 429 | A plan limit has been surpassed. |
| 5xx | Signifies a server error with Supadata. |

Refer to the [Error Codes](https://docs.supadata.ai/errors) section for a detailed explanation of all potential API errors.

## [​](https://docs.supadata.ai/api-reference/introduction\#rate-limit)  Rate limit

The Supadata API has a rate limit to ensure the stability and reliability of the service. The rate limit is applied to all endpoints and is based on the number of requests made within a specific time frame and your current subscription plan.When you exceed the rate limit, you will receive a 429 response code.

Was this page helpful?

YesNo

[Suggest edits](https://github.com/supadata-ai/supadata-docs/edit/main/api-reference/introduction.mdx) [Raise issue](https://github.com/supadata-ai/supadata-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/api-reference/introduction)

[Transcript](https://docs.supadata.ai/api-reference/endpoint/transcript/transcript)

Ctrl+I
