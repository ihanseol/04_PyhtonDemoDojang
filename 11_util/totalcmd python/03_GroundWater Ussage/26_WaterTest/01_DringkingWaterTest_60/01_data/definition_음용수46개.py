 def __init__(self, data: Dict[str, str]):
        """
        Initialize water quality data.

        Args:
            data: Dictionary containing water quality parameters
        """
        self._validate_data(data)

        self.general_bacteria = data['General_bacteria']        #일반세균
        self.total_coliform = data['Total_coliforms']            #총대장균군
        self.fecal_coliforms = data['Fecal_coliforms']          #대장균/분원성대장균군
        self.lead = data['Lead']                                #납
        self.fluoride = data['Fluoride']                        #불소
        self.arsenic = data['Arsenic']                          #비소
        self.selenium = data['Selenium']                        #세레늄
        self.mercury = data['Mercury']                          #수은
        self.cyanide = data['Cyanide']                          #시안
        self.chromium = data['Chromium']                        #크롬

        self.ammonia_nitrogen = data['Ammonia_nitrogen']        #암모니아성질소
        self.nitrate_nitrogen = data['Nitrate_nitrogen']        #질산성질소
        self.cadmium = data['Cadmium']                          #카드뮴
        self.boron = data['Boron']                              #붕소
        self.phenol = data['Phenol']                            #페놀

        self.diazinon = data['Diazinon']                        #다이아지논
        self.parathion = data['Parathion']                      #파라티논
        self.fenitrothion = data['Fenitrothion']                #페니트로티논
        self.carbaryl = data['Carbaryl']                        #카바릴

        self.trichloroethane = data['1,1,1-Trichloroethane']    #1,1,1-트리클로로에탄
        self.tetrachloroethylene = data['Tetrachloroethylene']  #테트라클로로에틸렌
        self.trichloroethylene = data['Trichloroethylene']      #트리클로로에틸렌
        self.dichloromethane = data['Dichloromethane']          #디클로로메탄

        self.benzene = data['Benzene']                          #벤젠
        self.toluene = data['Toluene']                          #톨루엔
        self.ethylbenzene = data['Ethylbenzene']                #에틸벤젠
        self.xylene = data['Xylene']                            #크실렌

        self.dichloroethylene = data['1,1-Dichloroethylene']                #1.1-디클로로에틸렌
        self.carbon_tetrachloride = data['Carbon_tetrachloride']            #사염화탄소
        self.dibromo_3_chloropropane = data['1,2-Dibromo-3-chloropropane']  #1.2-디브로모-3-클로로프로판
        self.dioxane = data['1,4-Dioxane']                                  #1.4-다이옥산

        self.hardness = data['Hardness']        #경도
        self.potassium_permanganate_consumption = data['Potassium_permanganate_consumption']  #과망간산칼륨소비량

        self.odor = data['Odor']                    #냄새
        self.taste = data['Taste']                  #맛
        self.copper = data['Copper']                #동
        self.color = data['Color']                  #색도

        self.detergents = data['Detergents']        #세제
        self.ph = data['pH']                        #수소이온농도

        self.zinc = data['Zinc']                    #아연
        self.chloride = data['Chloride_ion']        #염소이온
        self.iron = data['Iron']                    #철
        self.manganese = data['Manganese']          #망간
        self.turbidity = data['Turbidity']          #탁도
        self.sulfate_ion = data['Sulfate_ion']      #황산이온
        self.aluminum = data['Aluminum']            #알루미늄

        # Overall Result
        self.water_ok = data['water_ok']            #수질 적합, 부적합