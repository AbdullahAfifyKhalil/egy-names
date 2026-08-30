<?php

declare(strict_types=1);

namespace Afify\EgyNames;

/**
 * Egyptian names engine. Same behaviour as the TypeScript SDK, plus Python age features.
 */
class EgyptianNames
{
    public const VERSION = '0.3.4';

    public function __construct(private ?int $seed = null)
    {
    }

    public function __get(string $name): mixed
    {
        if ($name === 'batch') {
            return new BatchProcessor($this);
        }
        throw new \Error('Undefined property: ' . self::class . '::$' . $name);
    }

    public function batch(): BatchProcessor
    {
        return new BatchProcessor($this);
    }

    /**
     * @return list<GeneratedName>
     */
    public function generate(
        int $count = 1,
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $family_name = true,
        ?string $frequency = null,
        string $lang = 'both',
        ?int $seed = null,
    ): array {
        return Generator::generate(
            $count,
            $gender,
            $religion,
            $length,
            $family_name,
            $frequency,
            $lang,
            $seed ?? $this->seed,
        );
    }

    public function translate(string $name, ?string $to = null): string
    {
        return Translator::translate($name, $to);
    }

    public function lookup(string $name): ?NameInfo
    {
        $entry = Lookup::lookup($name);
        return $entry !== null ? NameInfo::fromEntry($entry) : null;
    }

    public function info(string $name): ?NameInfo
    {
        return $this->lookup($name);
    }

    /**
     * @return NameInfo|list<NameInfo|null>|null
     */
    public function annotate(string $name): NameInfo|array|null
    {
        return Annotator::annotate($name);
    }

    /**
     * @return list<string>
     */
    public function split(string $full_name): array
    {
        return Splitter::split($full_name);
    }

    public function tashkeel(string $name, string $dialect = 'standard'): string
    {
        if (trim($name) === '') {
            return '';
        }
        $rawTokens = preg_split('/\s+/u', trim($name)) ?: [];
        $result = [];
        $isEg = $dialect === 'egyptian';
        $n = count($rawTokens);

        for ($i = 0; $i < $n; $i++) {
            $current = $rawTokens[$i];

            if ($i < $n - 1) {
                $next = $rawTokens[$i + 1];
                $compound = $current . ' ' . $next;
                $compoundNoSpace = $current . $next;
                $compoundEntry = Lookup::lookupAr($compound) ?? Lookup::lookupAr($compoundNoSpace);
                if ($compoundEntry !== null) {
                    $val = $isEg ? $compoundEntry->tashkeelEg : $compoundEntry->tashkeelStandard;
                    if ($val !== '') {
                        $result[] = $val;
                        $i++;
                        continue;
                    }
                }
            }

            $entry = Lookup::lookupAr($current);
            if ($entry !== null) {
                $val = $isEg ? $entry->tashkeelEg : $entry->tashkeelStandard;
                $result[] = $val !== '' ? $val : $current;
            } else {
                $result[] = $current;
            }
        }

        return implode(' ', $result);
    }

    public function tashkeelEg(string $name): string
    {
        return $this->tashkeel($name, 'egyptian');
    }

    public function tashkeel_eg(string $name): string
    {
        return $this->tashkeelEg($name);
    }

    public function tashkeelStandard(string $name): string
    {
        return $this->tashkeel($name, 'standard');
    }

    public function tashkeel_standard(string $name): string
    {
        return $this->tashkeelStandard($name);
    }

    public function ipa(string $name, string $dialect = 'standard'): string
    {
        if (trim($name) === '') {
            return '';
        }
        $tokens = str_contains($name, ' ')
            ? (preg_split('/\s+/u', trim($name)) ?: [])
            : $this->split($name);
        $isEg = $dialect === 'egyptian';
        $ipaParts = [];

        foreach ($tokens as $tok) {
            $entry = Lookup::lookup($tok);
            if ($entry !== null) {
                $ipaVal = $isEg ? $entry->ipaEg : $entry->ipaStandard;
                if ($ipaVal !== '') {
                    $ipaParts[] = preg_replace('/^[\/\[\]]+|[\/\[\]]+$/u', '', $ipaVal) ?? $ipaVal;
                } else {
                    $ipaParts[] = $tok;
                }
            } else {
                $ipaParts[] = $tok;
            }
        }

        $joined = implode(' ', $ipaParts);
        return $isEg ? '[' . $joined . ']' : '/' . $joined . '/';
    }

    public function ipaEg(string $name): string
    {
        return $this->ipa($name, 'egyptian');
    }

    public function ipa_eg(string $name): string
    {
        return $this->ipaEg($name);
    }

    public function ipaStandard(string $name): string
    {
        return $this->ipa($name, 'standard');
    }

    public function ipa_standard(string $name): string
    {
        return $this->ipaStandard($name);
    }

    /**
     * @return list<string>
     */
    public function dallaa(string $name, string $format = 'plain'): array
    {
        $entry = Lookup::lookup($name);
        if ($entry === null) {
            return [];
        }
        $fmt = strtolower($format);
        if ($fmt === 'tashkeel' || $fmt === 'tashkeel_eg' || $fmt === 'tk') {
            return $entry->dallaaTashkeel !== [] ? $entry->dallaaTashkeel : $entry->dallaaAr;
        }
        if ($fmt === 'en' || $fmt === 'english') {
            return $entry->dallaaEn;
        }
        if ($fmt === 'ipa' || $fmt === 'phonetic') {
            return $entry->dallaaIpa;
        }
        return $entry->dallaaAr;
    }

    /**
     * @return list<PetName>
     */
    public function dallaaInfo(string $name): array
    {
        $entry = Lookup::lookup($name);
        if ($entry === null || $entry->dallaaAr === []) {
            return [];
        }
        $result = [];
        foreach ($entry->dallaaAr as $i => $ar) {
            $result[] = new PetName(
                $ar,
                $entry->dallaaTashkeel[$i] ?? $ar,
                $entry->dallaaEn[$i] ?? '',
                $entry->dallaaIpa[$i] ?? '',
            );
        }
        return $result;
    }

    /**
     * @return list<PetName>
     */
    public function dallaa_info(string $name): array
    {
        return $this->dallaaInfo($name);
    }

    /**
     * @return list<string>
     */
    public function petNames(string $name, string $format = 'plain'): array
    {
        return $this->dallaa($name, $format);
    }

    /**
     * @return list<string>
     */
    public function pet_names(string $name, string $format = 'plain'): array
    {
        return $this->petNames($name, $format);
    }

    public function root(string $name): ?string
    {
        $entry = Lookup::lookup($name);
        return $entry !== null && $entry->root !== 'N/A' ? $entry->root : null;
    }

    public function origin(string $name): ?string
    {
        $entry = Lookup::lookup($name);
        return $entry !== null ? $entry->originType : null;
    }

    /**
     * @return list<string>
     */
    public function famousFigures(string $name, string $lang = 'ar'): array
    {
        $entry = Lookup::lookup($name);
        if ($entry === null) {
            return [];
        }
        if (str_starts_with(strtolower($lang), 'en')) {
            return $entry->famousFiguresEn !== [] ? $entry->famousFiguresEn : $entry->famousFiguresAr;
        }
        return $entry->famousFiguresAr;
    }

    /**
     * @return list<string>
     */
    public function famous_figures(string $name, string $lang = 'ar'): array
    {
        return $this->famousFigures($name, $lang);
    }

    public function trend(string $name): ?string
    {
        $entry = Lookup::lookup($name);
        return $entry !== null ? $entry->trendCategory : null;
    }

    public function correct(string $name): string
    {
        return Corrector::correct($name);
    }

    /**
     * @return array{ar: string, en: string}|null
     */
    public function meaning(string $name): ?array
    {
        $entry = Lookup::lookup($name);
        if ($entry === null) {
            return null;
        }
        if ($entry->meaningAr === '' && $entry->meaningEn === '') {
            return null;
        }
        return [
            'ar' => $entry->meaningAr,
            'en' => $entry->meaningEn,
        ];
    }

    /**
     * @return list<NameInfo>
     */
    public function families(
        ?int $count = null,
        ?string $frequency = null,
        ?string $religion = null,
        ?string $starts_with = null,
    ): array {
        return Search::search(
            role: 'family',
            frequency: $frequency,
            religion: $religion,
            starts_with: $starts_with,
            max_results: $count ?? 50,
        );
    }

    /**
     * @return list<NameInfo>
     */
    public function search(
        ?string $gender = null,
        ?string $religion = null,
        ?string $role = null,
        ?string $frequency = null,
        ?string $starts_with = null,
        ?string $ends_with = null,
        ?string $prefix = null,
        ?string $suffix = null,
        ?string $contains = null,
        ?float $min_corpus_share = null,
        ?int $max_results = null,
        ?string $sort_by = null,
    ): array {
        return Search::search(
            $gender,
            $religion,
            $role,
            $frequency,
            $starts_with,
            $ends_with,
            $prefix,
            $suffix,
            $contains,
            $min_corpus_share,
            $max_results,
            $sort_by,
        );
    }

    public function isValid(string $name): bool
    {
        $entry = Lookup::lookup($name);
        return $entry !== null
            && Quality::isPersonalEntry($entry)
            && !Quality::isLowConfidenceEntry($entry);
    }

    public function is_valid(string $name): bool
    {
        return $this->isValid($name);
    }

    /**
     * Split on whitespace, but merge an adjacent pair into one lemma
     * when the book has it as a two-word compound (e.g. kunya "Abu X").
     *
     * @return list<array{0: string, 1: ?NameEntry}>
     */
    public function compoundTokens(string $fullName): array
    {
        $raw = preg_split('/\s+/u', trim($fullName), -1, PREG_SPLIT_NO_EMPTY) ?: [];
        $out = [];
        $i = 0;
        $n = count($raw);
        while ($i < $n) {
            if ($i < $n - 1) {
                $pair = $raw[$i] . ' ' . $raw[$i + 1];
                $pairEntry = Lookup::lookupAr($pair) ?? Lookup::lookupAr($raw[$i] . $raw[$i + 1]);
                if ($pairEntry !== null) {
                    $out[] = [$pair, $pairEntry];
                    $i += 2;
                    continue;
                }
            }
            $out[] = [$raw[$i], Lookup::lookup($raw[$i])];
            $i++;
        }
        return $out;
    }

    public function detectGender(string $full_name): GenderDetection
    {
        $tokens = $this->compoundTokens($full_name);
        if ($tokens === []) {
            return new GenderDetection('neutral', 0);
        }

        $skippedLineage = 0;
        foreach ($tokens as $i => [, $entry]) {
            if ($entry === null || !Quality::isPersonalEntry($entry) || Quality::isLowConfidenceEntry($entry)) {
                continue;
            }
            if (Quality::isLineage($entry)) {
                $skippedLineage++;
                continue;
            }
            if ($entry->gender === Gender::NEUTRAL) {
                return new GenderDetection('neutral', 0.6);
            }
            $confidence = ($skippedLineage === 0 && $i === 0) ? 1.0 : 0.85;
            return new GenderDetection($entry->gender->value, $confidence);
        }
        return new GenderDetection('neutral', 0);
    }

    public function detect_gender(string $full_name): GenderDetection
    {
        return $this->detectGender($full_name);
    }

    public function detectReligion(string $full_name): ReligionDetection
    {
        $tokens = $this->compoundTokens($full_name);
        if ($tokens === []) {
            return new ReligionDetection('neutral', 0);
        }

        $skippedLineage = 0;
        foreach ($tokens as $i => [, $entry]) {
            if ($entry === null || !Quality::isPersonalEntry($entry) || Quality::isLowConfidenceEntry($entry)) {
                continue;
            }
            if (Quality::isLineage($entry)) {
                $skippedLineage++;
                continue;
            }
            if ($entry->religion === Religion::NEUTRAL) {
                continue;
            }
            $confidence = ($skippedLineage === 0 && $i === 0) ? 1.0 : 0.9;
            return new ReligionDetection($entry->religion->value, $confidence);
        }

        // The person's own given names carried no distinctive signal
        // (neutral or not found). Fall back to an aggregate vote across
        // every token, lineage included, rather than declaring neutral.
        $muslim = 0.0;
        $christian = 0.0;
        $first = null;

        foreach ($tokens as [, $entry]) {
            if ($entry === null || !Quality::isPersonalEntry($entry) || Quality::isLowConfidenceEntry($entry)) {
                continue;
            }
            if ($entry->religion === Religion::MUSLIM) {
                $muslim++;
                if ($first === null) {
                    $first = 'muslim';
                }
            } elseif ($entry->religion === Religion::CHRISTIAN) {
                $christian++;
                if ($first === null) {
                    $first = 'christian';
                }
            }
        }

        if ($muslim === 0.0 && $christian === 0.0) {
            return new ReligionDetection('neutral', 0);
        }

        $distinctive = $muslim + $christian;
        if ($muslim > $christian) {
            return new ReligionDetection('muslim', 0.5 * $muslim / $distinctive);
        }
        if ($christian > $muslim) {
            return new ReligionDetection('christian', 0.5 * $christian / $distinctive);
        }
        return new ReligionDetection($first ?? 'neutral', 0.5);
    }

    public function detect_religion(string $full_name): ReligionDetection
    {
        return $this->detectReligion($full_name);
    }

    public function fingerprint(string $name): ?Fingerprint
    {
        $entry = Lookup::lookup($name);
        if ($entry === null) {
            return null;
        }

        $slots = $entry->slotPcts;
        $slotLabels = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th+'];

        $peakSlot = 0;
        $maxPct = -1.0;
        foreach ($slots as $i => $pct) {
            if ($pct > $maxPct) {
                $maxPct = $pct;
                $peakSlot = $i;
            }
        }

        if ($entry->role->isFamilyLike()) {
            $nameType = ($slots[0] ?? 0) < 1.0 ? 'pure_surname' : 'surname_given';
        } elseif ($peakSlot === 0 && ($slots[0] ?? 0) > 40) {
            $nameType = 'primary_given';
        } elseif ($peakSlot === 0) {
            $nameType = 'given_name';
        } else {
            $nameType = 'patronymic';
        }

        $descParts = [];
        if ($nameType === 'primary_given') {
            $descParts[] = 'Dominant first name (' . number_format($slots[0] ?? 0, 1, '.', '') . '% in slot 1)';
        } elseif ($nameType === 'pure_surname') {
            $descParts[] = 'Almost exclusively a family/surname';
        } elseif ($nameType === 'given_name') {
            $descParts[] = 'Given name appearing across multiple positions';
        } else {
            $descParts[] = 'Peaks in slot ' . ($peakSlot + 1);
        }

        if ($entry->frequency === FrequencyClass::COMMON) {
            $descParts[] = 'very common';
        } elseif ($entry->frequency === FrequencyClass::RARE) {
            $descParts[] = 'rare';
        }

        $slotMap = [];
        foreach ($slotLabels as $i => $label) {
            $slotMap[$label] = round(($slots[$i] ?? 0) * 100) / 100;
        }

        return new Fingerprint(
            $entry->ar,
            $entry->en,
            $nameType,
            $slotMap,
            $entry->corpusShare,
            implode('; ', $descParts),
        );
    }

    public function rank(string $name): ?RankInfo
    {
        $entry = Lookup::lookup($name);
        if ($entry === null) {
            return null;
        }

        $ranked = Lookup::getRanked();
        $total = count($ranked);

        foreach ($ranked as $i => $e) {
            if ($e->ar === $entry->ar) {
                $rankPos = $i + 1;
                $percentile = (1 - ($rankPos - 1) / $total) * 100;
                $desc = 'The #' . $rankPos . ' most common name in the Egyptian corpus';
                if ($rankPos <= 10) {
                    $desc = 'Top 10 — ' . $desc;
                } elseif ($rankPos <= 100) {
                    $desc = 'Top 100 — ' . $desc;
                } elseif ($rankPos <= 1000) {
                    $desc = 'Top 1000 — ' . $desc;
                }

                return new RankInfo(
                    $rankPos,
                    round($percentile * 100) / 100,
                    number_format($entry->corpusShare, 4, '.', '') . '%',
                    $desc,
                );
            }
        }
        return null;
    }

    /**
     * @return list<string>
     */
    public function similar(string $name, int $max_results = 10, int $max_distance = 3): array
    {
        $useAr = Lookup::isArabic($name);
        $entries = Lookup::getAll();
        $nameNorm = $useAr ? Lookup::normalizeAr($name) : Lookup::normalizeEn($name);

        $scored = [];
        foreach ($entries as $e) {
            $candidate = $useAr ? $e->ar : $e->en;
            $candNorm = $useAr ? Lookup::normalizeAr($candidate) : Lookup::normalizeEn($candidate);
            if ($candNorm === $nameNorm) {
                continue;
            }
            $dist = self::levenshtein($nameNorm, $candNorm);
            if ($dist <= $max_distance) {
                $scored[] = ['dist' => $dist, 'share' => $e->corpusShare, 'candidate' => $candidate];
            }
        }

        usort($scored, static function (array $a, array $b): int {
            if ($a['dist'] !== $b['dist']) {
                return $a['dist'] <=> $b['dist'];
            }
            return $b['share'] <=> $a['share'];
        });

        $out = [];
        foreach (array_slice($scored, 0, $max_results) as $s) {
            $out[] = $s['candidate'];
        }
        return $out;
    }

    /**
     * @return list<ChainPart>
     */
    public function analyzeChain(string $full_name): array
    {
        $tokens = preg_split('/\s+/u', trim($full_name)) ?: [];
        if ($tokens === [] || $tokens === ['']) {
            return [];
        }

        $parts = [];
        $n = count($tokens);
        for ($i = 0; $i < $n; $i++) {
            $t = $tokens[$i];
            $entry = Lookup::lookup($t);
            $slot = $i + 1;

            if ($i === 0) {
                $roleLabel = 'person';
                $detail = "The individual's given name";
            } elseif ($i === $n - 1 && $entry !== null && $entry->role->isFamilyLike()) {
                $roleLabel = 'family_name';
                $detail = 'Family/tribal surname';
            } elseif ($i === 1) {
                $roleLabel = 'father';
                $detail = "Father's name";
            } elseif ($i === 2) {
                $roleLabel = 'grandfather';
                $detail = 'Paternal grandfather';
            } elseif ($i === 3) {
                $roleLabel = 'great_grandfather';
                $detail = 'Great-grandfather';
            } else {
                $roleLabel = 'ancestor';
                $detail = 'Ancestor (generation ' . $i . ')';
            }

            $parts[] = new ChainPart($t, $slot, $roleLabel, $detail);
        }

        return $parts;
    }

    /**
     * @return list<ChainPart>
     */
    public function analyze_chain(string $full_name): array
    {
        return $this->analyzeChain($full_name);
    }

    public function uniqueness(string $full_name): UniquenessScore
    {
        $tokens = preg_split('/\s+/u', trim($full_name)) ?: [];
        if ($tokens === [] || $tokens === ['']) {
            return new UniquenessScore(0.5, 'unknown', 'Empty input');
        }

        $shares = [];
        $unknownCount = 0;
        foreach ($tokens as $t) {
            $entry = Lookup::lookup($t);
            if ($entry !== null) {
                $shares[] = $entry->corpusShare;
            } else {
                $unknownCount++;
            }
        }

        if ($shares === []) {
            return new UniquenessScore(1.0, 'unknown', 'None of the name parts are in the Egyptian corpus');
        }

        $logSum = 0.0;
        foreach ($shares as $s) {
            $logSum += log(max($s, 1e-9));
        }
        $logMean = $logSum / count($shares);

        $maxLog = 2.6;
        $minLog = -9.2;
        $score = 1.0 - ($logMean - $minLog) / ($maxLog - $minLog);
        $score = max(0.0, min(1.0, $score));
        $score = min(1.0, $score + $unknownCount * 0.15);

        if ($score < 0.2) {
            $label = 'extremely_common';
            $note = 'Each part is among the most common names nationally';
        } elseif ($score < 0.4) {
            $label = 'common';
            $note = 'Well-known name parts with high national frequency';
        } elseif ($score < 0.6) {
            $label = 'moderate';
            $note = 'A mix of common and less common name parts';
        } elseif ($score < 0.8) {
            $label = 'distinctive';
            $note = 'Contains uncommon or regionally specific names';
        } else {
            $label = 'highly_unique';
            $note = 'Rare name combination — distinctive family heritage';
        }

        return new UniquenessScore(round($score * 1000) / 1000, $label, $note);
    }

    public function format(string $full_name, string $style = 'full'): string|FormatResult
    {
        $tokens = preg_split('/\s+/u', trim($full_name)) ?: [];
        if ($tokens === [] || $tokens === ['']) {
            return $full_name;
        }

        if ($style === 'full') {
            return implode(' ', $tokens);
        }

        if ($style === 'first_last') {
            $first = $tokens[0];
            $last = count($tokens) > 1 ? $tokens[count($tokens) - 1] : '';
            return new FormatResult($first, $last);
        }

        if ($style === 'western') {
            $firstEn = Translator::translateToken($tokens[0], 'en');
            $lastEn = count($tokens) > 1 ? Translator::translateToken($tokens[count($tokens) - 1], 'en') : '';
            return trim($firstEn . ' ' . $lastEn);
        }

        if ($style === 'initials') {
            $initials = [];
            $lastIdx = count($tokens) - 1;
            for ($i = 0; $i < $lastIdx; $i++) {
                $ch = Lookup::chars($tokens[$i]);
                $initials[] = ($ch[0] ?? '') . '.';
            }
            $initials[] = $tokens[$lastIdx];
            return implode(' ', $initials);
        }

        return implode(' ', $tokens);
    }

    public function formatName(string $full_name, string $style = 'full'): string|FormatResult
    {
        return $this->format($full_name, $style);
    }

    public function format_name(string $full_name, string $style = 'full'): string|FormatResult
    {
        return $this->format($full_name, $style);
    }

    /**
     * @return list<string>
     */
    public function suggest(
        ?string $gender = null,
        ?string $religion = null,
        ?string $role = null,
        ?string $frequency = null,
        ?string $starts_with = null,
        int $count = 10,
    ): array {
        $results = Search::search(
            gender: $gender,
            religion: $religion,
            role: $role,
            frequency: $frequency,
            starts_with: $starts_with,
            max_results: $count,
        );
        $out = [];
        foreach ($results as $r) {
            $out[] = $r->ar;
        }
        return $out;
    }

    /**
     * @return array<string, mixed>
     */
    public function stats(): array
    {
        $meta = Catalog::metadata();
        $nested = $meta['metadata'] ?? [];
        unset($meta['metadata']);
        if (is_array($nested)) {
            $meta = array_merge($nested, $meta);
        }
        $entries = Lookup::getAll();
        $given = 0;
        $family = 0;
        $male = 0;
        $female = 0;

        foreach ($entries as $e) {
            if ($e->role === NameRole::GIVEN) {
                $given++;
            }
            if ($e->role === NameRole::FAMILY) {
                $family++;
            }
            if ($e->gender === Gender::MALE) {
                $male++;
            }
            if ($e->gender === Gender::FEMALE) {
                $female++;
            }
        }

        return array_merge($meta, [
            'total_names' => count($entries),
            'given_names' => $given,
            'family_names' => $family,
            'male_names' => $male,
            'female_names' => $female,
        ]);
    }

    /**
     * @return list<NameInfo>
     */
    public function namesForAge(
        int $age,
        ?string $gender = null,
        ?int $as_of_year = null,
        int $top = 20,
        bool $include_family = false,
    ): array {
        $entries = Age::namesForAge($age, $gender, $as_of_year, $top, $include_family);
        $out = [];
        foreach ($entries as $e) {
            $out[] = NameInfo::fromEntry($e);
        }
        return $out;
    }

    /**
     * @return list<NameInfo>
     */
    public function names_for_age(
        int $age,
        ?string $gender = null,
        ?int $as_of_year = null,
        int $top = 20,
        bool $include_family = false,
    ): array {
        return $this->namesForAge($age, $gender, $as_of_year, $top, $include_family);
    }

    public function ageProfile(string $name): ?AgeProfile
    {
        $entry = Lookup::lookup($name);
        if ($entry === null) {
            return null;
        }
        return Age::ageProfile($entry);
    }

    public function age_profile(string $name): ?AgeProfile
    {
        return $this->ageProfile($name);
    }

    public function detectAge(string $name, ?int $as_of_year = null): ?AgeDetection
    {
        $tokens = preg_split('/\s+/u', trim($name)) ?: [];
        if ($tokens === [] || $tokens === ['']) {
            return null;
        }

        $tokenEntries = [];
        $slotIdx = 0;
        foreach ($tokens as $token) {
            $entry = Lookup::lookup($token);
            if ($entry !== null) {
                $tokenEntries[] = [$entry, $slotIdx];
                $slotIdx++;
            }
        }

        if ($tokenEntries === []) {
            return null;
        }

        return Age::detectAgeFromChain($tokenEntries, $as_of_year);
    }

    public function detect_age(string $name, ?int $as_of_year = null): ?AgeDetection
    {
        return $this->detectAge($name, $as_of_year);
    }

    private static function levenshtein(string $s1, string $s2): int
    {
        $a = Lookup::chars($s1);
        $b = Lookup::chars($s2);
        if (count($a) < count($b)) {
            return self::levenshtein($s2, $s1);
        }
        if ($b === []) {
            return count($a);
        }

        $prevRow = range(0, count($b));
        foreach ($a as $i => $ca) {
            $currRow = [$i + 1];
            foreach ($b as $j => $cb) {
                $insertions = $prevRow[$j + 1] + 1;
                $deletions = $currRow[$j] + 1;
                $substitutions = $prevRow[$j] + ($ca !== $cb ? 1 : 0);
                $currRow[] = min($insertions, $deletions, $substitutions);
            }
            $prevRow = $currRow;
        }
        return $prevRow[count($prevRow) - 1];
    }
}
