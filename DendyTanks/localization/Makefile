SOURCEDIR = ..
DOMAIN = all
LOCALE = ru

translate_ru: $(LOCALE)/LC_MESSAGES/$(DOMAIN).mo

$(LOCALE)/LC_MESSAGES/$(DOMAIN).mo: $(LOCALE)/LC_MESSAGES/$(DOMAIN).po
	pybabel compile -D $(DOMAIN) -d . -l $(LOCALE)

$(LOCALE)/LC_MESSAGES/$(DOMAIN).po: $(DOMAIN).po
	pybabel update -D $(DOMAIN) -i $(DOMAIN).po -l $(LOCALE) -d .

$(DOMAIN).po: $(SOURCEDIR)/*.py #actually only Localization.py
	pybabel extract $(SOURCEDIR) -o $(DOMAIN).po