# Stella - A language learning helper bot

Stella is a Discord Bot that aims to help language learners. It currently houses two functions.

```
COMMAND NAME            COMMAND FUNCTION
------------------------------------------------------------------------------

?q [lang_code]          Asks a very simple question that is meant 
                        to be answered by learners at CEFR level A2 or below.  

?topic [lang_code]      Asks a question that is meant to start a discussion.
                        Meant to encourage conversation of learners of 
                        CEFR level B1 or up.
                        The argument [lang_code] specifies the language of
                        the question asked. Otherwise, the default language
                        of the server is used. See ?deflang

?deflang [lang_code]    Sets the default language of the given server
ADMIN ONLY              to [lang_code]. The default value is 'en' for English.

NOTE: Language codes follow the ISO 691-1 standard. If the language is not found
in ISO 691-1, then ISO 639-3 is used.
```