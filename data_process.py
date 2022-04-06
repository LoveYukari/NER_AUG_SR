import os
import codecs
import argparse
import re
from data_aug import synonym_replacement


def load_file(file_path):
    if not os.path.exists(file_path):
        return None
    with codecs.open(file_path, 'r', encoding='utf-8') as fd:
        for line in fd:
            yield line


def _cut(sentence):
    new_sentence = []
    sen = []
    for i in sentence:
        if i.split(' ')[0] in ['。', '！', '？'] and len(sen) != 0:
            sen.append(i)
            new_sentence.append(sen)
            sen = []
            continue
        sen.append(i)
    if len(new_sentence) == 1:  # 娄底那种一句话超过max_seq_length的且没有句号的，用,分割，再长的不考虑了。。。
        new_sentence = []
        sen = []
        for i in sentence:
            if i.split(' ')[0] in ['，'] and len(sen) != 0:
                sen.append(i)
                new_sentence.append(sen)
                sen = []
                continue
            sen.append(i)
    return new_sentence


def cut_sentence(file, max_seq_length):
    """
    句子截断
    :param file: 
    :param max_seq_length: 
    :return: 
    """
    context = []
    sentence = []
    ctx_label = []
    label = []
    cnt = 0
    for line in load_file(file):
        line = line.strip()
        if line == '' and len(sentence) != 0:
            # 判断这一句是否超过最大长度
            if len(sentence) > max_seq_length:
                sentence = _cut(sentence)
                ctx_label = _cut(ctx_label)
                context.extend(sentence)
                label.extend(ctx_label)
            else:
                context.append(sentence)
                label.append(ctx_label)
            sentence = []
            ctx_label = []
            continue
        cnt += 1
        sentence.append(re.search(r'(?<!\t)\S+', line).group(0))
        ctx_label.append((re.search(r'(?<=\t)\S+', line).group(0)))
    print('token cnt:{}'.format(cnt))
    return context, label


def write_to_file(file, context):
    # 首先将源文件改名为新文件名，避免覆盖
    os.rename(file, '{}.bak'.format(file))
    with codecs.open(file, 'w', encoding='utf-8') as fd:
        for sen in context:
            for token in sen:
                fd.write(token + '\n')
            fd.write('\n')


if __name__ == '__main__':
    words, labels = cut_sentence("few_shot\\train.tsv", 256)
    with codecs.open("few_shot\\AUG4.TSV", 'w', encoding='utf-8') as fd:
        for i in range(len(words)):
            new_words, new_labels = synonym_replacement(words[i], labels[i], n=len(words)/3)
        # 有个同义词替换BUG,换同义词的时候是全部替换,导致前面刚换的同义词会被一起替换了,有空再改
            while len(new_words) != len(new_labels):
                new_words, new_labels = synonym_replacement(
                words[i], labels[i], n=len(words)/3)
            for j in range(len(new_words)):
                try:
                    fd.write(new_words[j]+"\t"+new_labels[j])
                except:
                    raise ValueError(f"Wrong in : {i}")
                fd.write('\n')
            fd.write('\n')
    # new_words,new_labels=synonym_replacement(words[5423],labels[5423],n=len(words)/3)
    # print(new_words,new_labels)
    # print(len(new_words),'+',len(new_labels))
    # write_to_file("NCBI-disease-IOB\\train.tsv",new_words)
    # words[133]
