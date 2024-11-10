# Zoe

Text-based Natural Language Calendar Management System
===========================================

## Introduction

Zoe is an NLP system for managing calendar operations, specifically scheduling,
canceling, and searching for events while handling casual small talk through the command line.

## Working with Zoe

Follow Zoe's prompts and experiment using the code to understand its usage.

See below for a cheat sheet on using Zoe with single-turn prompts.

### Booking Calendar Events

Sample query: `Book "meeting with Eden" at 1.30pm tomorrow`

Sample query: `Book "meeting with Jony" on 01/29/2023 at 10pm`

_note: event names are in quotes_

### Searching Calendar Events

Sample query: `Show all my events for tomorrow` / `Show tomorrow`

### Cancelling Calendar Events

Sample query: Cancel "meeting with Jony" on 01/29/2024 at 10pm

_note: event names are in quotes_

## Extensibility

Zoe's capabilities are extensible.
New intents are introduced through the following steps:

1. Create an intent set in the `intent_sets` directory with the intents’ name as the filename and the associated
   prompts as its file contents.
2. Logic for intent sets are processed using `intent handlers` and stored in the `intent_handlers` directory. Create an
   intent handler for your intent set.
3. Retrain Zoe's classifier using the `reindex` flag.

## High-level Architecture (UML)

![Zoe UML diagram.jpg](assets/UML%20diagram.jpg)

## License

Zoe is [GPL-2](https://github.com/abeljohny/Zoe/blob/00873ef0f5696fbaf467b30bcb65f93f02a5656e/LICENSE) licensed.
