# AI services

## Rekognition

Image recognition service that finds objects, people, text, scenes in images
and video. For human, facial analysis and search (user verification, counting)
is possible. It helps to create a database of familiar faces or compare against
celebrities. Other use cases including labeling, content moderation, sport
analysis (pathing i.e. next moving direction) and etc.

> content moderation including inapproproate, unwanted or offensive materials
> and can be used in social media, broadcast media, ads, ecommerce and etc. for
> better user experience. there is a minimum confidence threshold setting that
> can help with the filtering. flagged content can be manually reviewed in
> Amazon Augmented AI UI (A2I).

## Transcribe

Convert speech to text using deep learning automatic speech recognition (ASR).
It is possible to remove Personally Identifiable Information (PII) using
Redaction. Automatic language identification is possible for multi-lingual
audio. A few use cases including transcribe customer service call, auto
subtitling and generate metadata for media assets for searchable archive.

## Polly

Turn text into speech using deep learning and supports lexicon and SSML.
Lexicon allows customization of the pronunciation of words with pronunciation
lexicons e.g.

- stylized words `St3v3` => `steve`
- acronyms `aws` => `amazon web services`

SSML or speech synthesis markup language allows

- emphasizing specific words or phrases
- using phonetic pronunciation
- include breathing or whispering
- using Newscaster speaking style
  
> note SSML and lexicon can be used together

## Translate

Translate between languages to enable localized content of websites and apps.
It can translate large volume of text efficiently.

## Lex+Connect

Lex is the technology that power Alexa, which does ASR (speech to text) and NLU
to recognize intent of users. It helps to build chatbots or call center bots.
Connect is a cloud based virtual contact center service to receive calls,
create contact flows. Connect integrates well wtih CRM systems and AWS. It
offers no upfront payments and is estimated cheaper compared to traditional
call centers.

flow of scheduling an appointment

![lex-connect](lex-connect.PNG)

## Comprehend

Fully managed serverless service that does NLP stuff or understand stuffs. It
can

- understand language of text
- extract key phrases/places/people/brands/events etc
- sentiment analysis
- analyze text using tokenization and part of speech
- organize collection of text files by topic

A few use cases including

- analysize customer feedback to understand what gives good/bad experience
- create and group articles by topics

### Comprehend Medical

To understand clinical text including physicial notes, discharge summaries,
test results, case notes and etc by using NLP to detect protected health info.

## SageMaker

Fully managed service to build ML pipeline from model building, data cleaning
training and deployment.

## Forecast

Fully managed service to deliver high accuracy forecast. Is used for product
demand planning, financial planning, resource planning and etc.

## Kendra

Fully managed document search service to extract answers within documents (
text, pdf, html, pptx, word and etc.). Kendra creates an index powered by ML
for subsequent search. It is also possible to learn from interactions/feedbacks
to promote preferred results (incremental learning). Customization is also
possible for search result fine tuning i.e. importance of data, freshness etc.

## Personalize

Fully managed real time recsys service for personal recommendations. It
integrates existing websites, apps, SMS, email marketing systems etc and allow
implementation in days.

## Textract

Extract text from various input type images/pdf with use cases e.g. driver
license data extraction etc.