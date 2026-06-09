from Variable import Variable
from bn_template import BayesianNetwork
from Runner import print_marginal_probabilities, print_conditional_probability


def create_car_network() -> BayesianNetwork:
    dt_prob = {(): (0.7, 0.3)}
    em_prob = {(): (0.7, 0.3)}
    ftl_prob = {(): (0.8, 0.2)}

    v_prob = {
        ('false',): (0.9, 0.1),
        ('true',):  (0.3, 0.7),
    }

    sms_prob = {
        ('false', 'false'): (0.3, 0.7),
        ('true',  'false'): (0.4, 0.6),
        ('false', 'true'):  (0.7, 0.3),
        ('true',  'true'):  (0.95, 0.05),
    }

    hc_prob = {
        ('false', 'false', 'false'): (0.99, 0.01),
        ('true',  'false', 'false'): (0.8,  0.2),
        ('false', 'true',  'false'): (0.5,  0.5),
        ('true',  'true',  'false'): (0.2,  0.8),
        ('false', 'false', 'true'):  (0.9,  0.1),
        ('true',  'false', 'true'):  (0.7,  0.3),
        ('false', 'true',  'true'):  (0.4,  0.6),
        ('true',  'true',  'true'):  (0.1,  0.9),
    }

    dt  = Variable('DT',  ('false', 'true'), dt_prob)
    em  = Variable('EM',  ('false', 'true'), em_prob)
    ftl = Variable('FTL', ('false', 'true'), ftl_prob)
    v   = Variable('V',   ('false', 'true'), v_prob,   [dt])
    sms = Variable('SMS', ('false', 'true'), sms_prob, [dt, em])
    hc  = Variable('HC',  ('false', 'true'), hc_prob,  [dt, em, ftl])

    network = BayesianNetwork()
    network.set_variables([dt, em, ftl, v, sms, hc])
    return network


def main():
    network = create_car_network()
    print_marginal_probabilities(network)
    print()

    print('=== Task 1: P(SMS=true | DT=true, EM=false) ===')
    print_conditional_probability(
        network,
        {'SMS': 'true'},
        {'DT': 'true', 'EM': 'false'},
    )

    print('=== Task 2: Diagnosis (V=true, SMS=true, HC=false) ===')
    symptoms = {'V': 'true', 'SMS': 'true', 'HC': 'false'}

    for cause in ['DT', 'EM', 'FTL']:
        print_conditional_probability(
            network,
            {cause: 'true'},
            symptoms,
        )


if __name__ == '__main__':
    main()
