from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np

### Uncomment to download required corpora/lexicons/models on first time running
# nltk.download('punkt')
# nltk.download('vader_lexicon')

corpus="""
Although the UK’s regression from EU environmental standards, revealed by the Guardian, seems very technical, the scale of the law changes means environmental legislation in Britain is facing death by a thousand cuts. In practice, changes by the EU that the UK is not following and planned divergences from EU law will mean toxic chemicals banned in the EU will be allowed to be used in the UK, the UK will reduce greenhouse gas emissions more slowly, its waters will be dirtier, and consumer products will be more likely to contribute to global deforestation. Here are some of the main differences:
Chemical regulations Law change: The UK has left the EU chemical regulation body, called EU Reach, which works quickly to ban substances found to be toxic to human health. After Brexit, the UK started its own smaller version, called UK Reach. Eight rules restricting the use of hazardous chemicals have been adopted by the EU since Brexit, and a further 16 are in the pipeline. The UK, however, has not banned any substances in that time and is considering only two restrictions: on lead ammunition, and harmful substances in tattoo ink. Bans on chemicals are generally preceded by a listing on the Reach bodies’ “substances of very high concern” list. The last additions to the UK’s list were made more than three years ago, in June 2020. Since then, the European Chemicals Agency has added 26 substances to its equivalent list.
These are primarily substances that are carcinogenic or affect the reproductive system, as well as being persistent in the environment and bioaccumulative. They are largely chemicals used in manufacturing, such as bis(4-chlorophenyl) sulphone which is used for making plastics, and melamine, a plastic used for reusable plates. What it means: Dangerous toxins proscribed in the EU will continue to be used in the UK. Trade with the EU could be adversely affected if UK companies use products banned in the bloc.
Pesticides Law change: The UK has not banned 36 harmful pesticides that have been proscribed for use in the EU. Thirty of the 36 were allowed for use in the EU when the UK left on 31 January 2020 but have since been banned by the bloc, and the remaining six have been approved by the UK government but not the EU since then. The best-known of these pesticide is thiamethoxam, a neonicotinoid that is highly toxic to bees and can remain in the soil long after treated seeds are planted. The UK has permitted its use every year since Brexit, while the EU has banned it. What it means: These pesticides are mostly banned for the harm they do to the environment and the insects, fish and other animals that live within it. It means farmers in the UK can use products that have been shown to harm invertebrate and insect populations. High carbon dioxide goods Law change: The EU has implemented a tariff on high-CO2 products, known as a carbon border adjustment mechanism, in an attempt to lower the bloc’s emissions. It will apply to high-CO2 products such as cement, iron and steel, aluminium, fertilisers, electricity and hydrogen in its first phase. Charging will begin in 2026, while the UK’s scheme, criticised as more lax by conservationists, has just been announced, is not in law and will not start until 2027 at the earliest. What it means: UK imports may be more polluting than those coming into the EU. Deforestation Law change: The EU has legislated to remove deforestation from its supply chain for products including wood, rubber, beef, leather, cocoa, coffee, palm oil and soy, meaning products will not make it into the bloc unless they can be shown to be deforestation-free. The UK’s recently announced scheme applies only to illegal deforestation, and leaves out some popular products including coffee. What it means: Critics have said that the UK scheme has a “perverse incentive” for countries to legalise deforestation, as only products created as a result of illegal deforestation fall under the ban. Regardless of this, it means products imported into the UK can be causing devastating deforestation, even if not illegal. Social climate fund Law change: A social climate fund that protects the most vulnerable people from the costs of the green transition has been legislated for in the EU. It can be used for direct income support and investments in energy-efficient building renovations and sustainable transport. In theory, governments could use it to subsidise train travel. There is nothing comparable in the UK. What it means: People in the EU will be able to make climate-friendly choices more easily than in the UK, where costs remain high for purchases including home insulation and rail tickets. Genetic modification Law change: The UK has implemented the Genetic Technology (Precision Breeding) Act to improve efficiency for farmers, to grow plants and breed animals that yield more profit. The EU has no such act and has tighter restrictions around genetically modified goods. What it means: This loosens the regulations on genetically modified plants and animals, which campaigners have said could be bad for animal welfare if they are genetically modified in an extreme way. Critics also say the legislation has been drafted in a loose way, with some saying it could apply to pets, which could be modified to have extreme features. Air pollution The law change: Ministers have proposed loosening Britain’s air pollution regulations under the UK’s Retained EU Law Act. The government has weakened the EU-derived national emissions ceiling directive, which the watchdog has said will cause UK air quality to decline. The parts of the regulations proposed for deletion require the government to prepare and implement its plan to reduce pollutants like nitrogen oxides and ammonia, and to review it if emissions are projected to exceed targets. What it means: Air in the UK will be legally allowed to be dirtier than that in the EU. Battery recycling The law change: Batteries in the EU have been subject to further regulation since the UK left the bloc, with a digital passport, due diligence policy, waste collection targets and minimum content levels. The UK is still in the consultation phase for its post-Brexit legislation. What it means: Batteries in the EU will be recycled in a more environmentally friendly way than in the UK. Some new laws are coming down the pipeline, with further and in some cases more serious regressions due to take place. There are legislative changes all the time, and with the UK and EU no longer in sync, there are dozens of areas where UK and EU environmental law was drafted to be almost identical that can now be changed. Below is what is happening as of now. Water quality Proposed changes: Ministers have been making plans to remove the EU’s water framework directive from legally binding targets, which legislates to force member states to clean up dirty rivers and seas from agricultural, chemical and sewage pollution. There have also been plans in place to regress from the habitats directive, which protects the habitats of rare wildlife in the EU, so that property developers could freely pollute nearby waterways. This has been shelved for now but the government has indicated that it could undo this rule in future. Under the EU’s urban waste water treatment directive, micropollutants and microplastics are set to be further regulated in the EU, which means England, Scotland and Wales will also fall behind. Northern Ireland has to remain aligned with EU standards under the protocol on this measure. The EU also plans to further regulate groundwater pollutants including PFAS “forever chemicals”, some pesticides and pharmaceuticals. The UK has no such plans. What they mean: Our rivers and seas would be allowed to be more polluted than that in the EU if these changes go ahead. Agricultural emissions Proposed changes: The industrial emissions directive, which commits European Union member states to control and reduce the impact of industrial emissions on the environment, is set to be amended to include intensive farming including cattle, pigs, and poultry. What they mean: Farming in the EU would produce fewer emissions than in the UK. Air pollution Proposed changes: The EU is set to strengthen the ambient air quality directive, which sets concentration limits for certain pollutants that are considered harmful including nitrogen dioxide (NO2) and small particulate matter. The EU is also debating whether to further regulate ozone-depleting substances. What they mean: Air quality in the EU would have tighter legal constraints than in the UK. The particulates the EU is considering strengthening the law over cause myriad health problems from asthma to cancer. Rare materials Proposed changes: Another EU regulation coming down the pipeline is the Critical Raw Materials Act, which covers 34 industrially significant materials important for the construction and production of wind farms, batteries and solar panels. Extracting them is often detrimental to the environment, so the EU is proposing a regulation setting targets on extraction, processing, recycling and consumption. The UK’s proposed strategy is weaker, only promising an investigation into producing some money to support supply chains. What they mean: The way the UK extracts, uses and disposes of materials used for green industry will be more polluting and less sustainable than that used by the EU. Fast fashion and food waste Proposed changes: The European parliament has proposed a revision to the waste framework directive focusing on textiles and food waste. What they mean: The way clothes and food is disposed of would be more tightly regulated in the EU than the UK, potentially meaning there would be more waste in the UK, which has implications for carbon emissions as well as landfill. Electrical recycling Proposed changes: A ruling regarding the waste electrical and electronic equipment recycling directive is likely to apply in the EU but not the UK. This tightens rules for waste recycling, and was proposed before Brexit. The European court of justice is deciding whether it will apply in the UK. What they mean: If it is decided this does not apply in the UK, electronics recycling in the UK will face laxer standards than in the EU, potentially leading to more waste and landfill.
"""

sentences=tokenize.sent_tokenize(corpus)

sentiments=[
    "negative",
    "neutral",
    "positive",
    "compound"
]

article_sentiment=np.empty((0,4))

for sentence in sentences:
    sentence_sentiment=np.array([])
    sia=SentimentIntensityAnalyzer()
    sentiment_dict=sia.polarity_scores(sentence)
    for sentiment_key in sentiment_dict:
        sentence_sentiment=np.append(sentence_sentiment,sentiment_dict[sentiment_key])
    
    article_sentiment=np.append(article_sentiment,np.array([sentence_sentiment]),axis=0)

avg_article_sentiment=article_sentiment.mean(axis=0)

print(avg_article_sentiment)

