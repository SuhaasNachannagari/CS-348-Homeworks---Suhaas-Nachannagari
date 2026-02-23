# Use this file to write your queries. Submit this file to Gradescope after finishing your homework.

# To run the autograder: `python3 manage.py run`

# The autograder will verify that your strings are in the correct format and will test your queries using a sample database.

# Your Gradescope submission will be tested against a different database. 

import sys

'''
Instructions:
Please put the queries under the corresponding strings below.
Example:
    query1 = r"""
    $a \leftarrow \text{place p} \bowtie \text{host h}$
    $a$
    """
'''


query1 = r"""
        $a \leftarrow \sigma_{\text{r.year} = 1950}(\text{races r})$
        $b \leftarrow \pi_{\text{a.name, a.date}}(a)$
        $b$
"""

query2 = r"""
        $a \leftarrow races r \times constructors c$
        $b \leftarrow \pi_{a.c_name, a.r_name}(a)$
        $b$
"""
query3 = r"""
        $a \leftarrow races r \bowtie_{r.raceid = re.raceid} results re$
        $b \leftarrow \sigma_{a.positionorder = 1 \land a.name = 'Monaco Grand Prix'}(a)$
        $c \leftarrow \pi_{b.driverid, b.name, b.date}(b)$
        $c$
"""

query4 = r"""
        $r_1 \leftarrow \sigma_{r.name = 'Monaco Grand Prix'}(races\ r)$
        $re_1 \leftarrow \sigma_{re.positionorder = 1}(results\ re)$
        $a \leftarrow r_1 \bowtie_{r_1.raceid = re_1.raceid} re_1$
        $b \leftarrow \pi_{a.driverid, a.name, a.date}(a)$
        $b$
"""

query5 = r"""
        $r_1 \leftarrow \sigma_{r.name = 'Monaco Grand Prix'}(races\ r)$
        $re_1 \leftarrow \sigma_{re.positionorder = 1}(results\ re)$
        $a \leftarrow re_1 \times r_1$
        $b \leftarrow \sigma_{a.r_1_raceid = a.re_1_raceid}(a)$
        $c \leftarrow \pi_{b.driverid, b.name, b.date}(b)$
        $c$
"""

query6 = r"""
        $a \leftarrow \pi_{c.constructorId, c.name}(\text{constructors c})$
        $b \leftarrow \sigma_{re.positionOrder = 1}(\text{results re})$
        $c \leftarrow \pi_{b.constructorId}(b)$
        $d \leftarrow \pi_{a.constructorId}(a)$
        $e \leftarrow d - c$
        $f \leftarrow a \ \theta_{a.constructorId = e.constructorId}\ e$
        $g \leftarrow \pi_{f.name}(f)$
        $g$
"""

query7 = r"""
        $a_1 \leftarrow \pi_{re.driverid}(\sigma_{re.position= 1}(\text{results re}))$
        $a_2 \leftarrow \pi_{re.driverid}(\sigma_{re.position = 2}(\text{results re}))$
        $a_3 \leftarrow \pi_{re.driverid}(\sigma_{re.position = 3}(\text{results re}))$
        $a_4 \leftarrow \pi_{re.driverid}(\sigma_{re.position = 4}(\text{results re}))$
        $a_5 \leftarrow \pi_{re.driverid}(\sigma_{re.position = 5}(\text{results re}))$
        $a_6 \leftarrow \pi_{re.driverid}(\sigma_{re.position = 6}(\text{results re}))$
        $a_7 \leftarrow \pi_{re.driverid}(\sigma_{re.position = 7}(\text{results re}))$
        $a_8 \leftarrow \pi_{re.driverid}(\sigma_{re.position = 8}(\text{results re}))$
        $a_9 \leftarrow \pi_{re.driverid}(\sigma_{re.position = 9}(\text{results re}))$
        $a_10 \leftarrow \pi_{re.driverid}(\sigma_{re.position = 10}(\text{results re}))$
        $b \leftarrow a_1 \cap a_2$
        $c \leftarrow b \cap a_3$
        $d \leftarrow c \cap a_4$
        $e \leftarrow d \cap a_5$
        $f \leftarrow e \cap a_6$
        $g \leftarrow f \cap a_7$
        $h \leftarrow g \cap a_8$
        $i \leftarrow h \cap a_9$
        $j \leftarrow i \cap a_10$
        $k \leftarrow \text{drivers dr} \ \theta_{\text{dr.driverid}=\text{j.driverid}} \ j$
        $\pi_{k.dr_driverid,\ k.surname}(k)$
"""

query8 = r"""
        $a \leftarrow \sigma_{\text{c.name} = 'BMW Sauber'}(\text{constructors c})$
        $b \leftarrow \sigma_{\text{c.name} = 'Toyota'}(\text{constructors c})$
        $c \leftarrow a \;\theta_{\text{a.constructorId = r.constructorId}}\; \text{results r}$
        $d \leftarrow b \;\theta_{\text{b.constructorId = r.constructorId}}\; \text{results r}$
        $e \leftarrow \pi_{\text{c.driverId}}(c)$
        $f \leftarrow \pi_{\text{d.driverId}}(d)$
        $g \leftarrow e \cap f$
        $h \leftarrow \text{drivers dr} \;\theta_{\text{dr.driverId = g.driverId}}\; g$
        $\pi_{\text{h.dr\_driverId}, \text{h.surname}}(h)$
"""

query9 = r"""
        $a \leftarrow \sigma_{\text{c.name} = 'BMW Sauber'}(\text{constructors c})$
        $b \leftarrow \sigma_{\text{c.name} = 'Toyota'}(\text{constructors c})$
        $c \leftarrow \sigma_{\text{c.name} \neq 'Toyota' \; \text{and} \; \text{c.name} \neq 'BMW Sauber'}(\text{constructors c})$
        $d \leftarrow a \;\theta_{\text{a.constructorId = r.constructorId}}\; \text{results r}$
        $e \leftarrow b \;\theta_{\text{b.constructorId = r.constructorId}}\; \text{results r}$
        $f \leftarrow c \;\theta_{\text{c.constructorId = r.constructorId}}\; \text{results r}$
        $g \leftarrow \pi_{\text{d.driverId}}(d)$
        $h \leftarrow \pi_{\text{e.driverId}}(e)$
        $i \leftarrow \pi_{\text{f.driverId}}(f)$
        $j \leftarrow g \cap h$
        $k \leftarrow j - i$
        $l \leftarrow \text{drivers dr} \;\theta_{\text{dr.driverId = k.driverId}}\; k$
        $\pi_{\text{l.dr\_driverId}, \text{l.surname}}(l)$
"""



# Do not edit below

queries = {
    "query1": query1,
    "query2": query2,
    "query3": query3,
    "query4": query4,
    "query5": query5,
    "query6": query6,
    "query7": query7,
    "query8": query8,
    "query9": query9,
}

def getQueries():
    for key in sorted(queries.keys()):
        if not isinstance(queries[key], str):
            print(f"Error: {key} is not a string.")
            sys.exit(1)

    return queries